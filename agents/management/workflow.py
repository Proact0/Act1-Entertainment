import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logging.getLogger().setLevel(logging.INFO)
from langgraph.graph import StateGraph

from agents.base_workflow import BaseWorkflow
from agents.management.modules.nodes import InstagramContentVerificationNode
from agents.management.modules.state import ManagementState
from agents.management.modules.conditions import route_based_on_intent


class ManagementWorkflow(BaseWorkflow):
    """
    콘텐츠 관리를 위한 Workflow 클래스

    이 클래스는 프로젝트, 팀, 리소스의 관리와 크리에이터 직업 성장을 위한 Workflow를 정의합니다.
    BaseWorkflow를 상속받아 기본 구조를 구현하고, ManagementState를 사용하여 상태를 관리합니다.
    LLM을 사용한 의도 분류와 MCP 서버를 통한 인스타그램 컨텐츠 검증 기능을 포함합니다.
    """

    def __init__(self, state):
        super().__init__()
        self.state = state

    def build(self):
        """
        관리 Workflow 그래프 구축 메서드

        StateGraph를 사용하여 콘텐츠 관리를 위한 Workflow 그래프를 구축합니다.
        LLM 기반 의도 분류, 인스타그램 컨텐츠 검증, 일반 응답 노드를 포함하며,
        조건부 라우팅을 통해 요청 유형에 따라 적절한 노드로 분기합니다.

        Returns:
            CompiledStateGraph: 컴파일된 상태 그래프 객체
        """
        
        def entry_point_inspector(state):
            """
            그래프의 실제 진입점에서 state를 검사하기 위한 디버깅 함수.
            """
            print(f"--- DEBUG: ENTRY POINT STATE ---")
            print(f"State type: {type(state)}")
            print(f"State keys: {state.keys() if hasattr(state, 'keys') else 'No keys'}")
            print(f"State content: {state}")
            print(f"---------------------------------")
            
            # LangGraph Studio에서 입력이 'input' 키로 전달되는 경우를 처리
            if isinstance(state, dict) and 'input' in state:
                # input 키의 내용을 최상위로 복사
                input_data = state['input']
                if isinstance(input_data, dict):
                    state.update(input_data)
                    print(f"Updated state with input data: {state}")
            
            # 만약 user_input이 없으면 기본값 설정
            if isinstance(state, dict) and 'user_input' not in state:
                state['user_input'] = ""
                print(f"Set default user_input: {state}")
            
            return state

        def general_response_node(state):
            """
            일반적인 질문이나 다른 작업에 대한 응답 노드
            """
            from agents.management.modules.models import get_gemini_model
            
            user_input = state.get("user_input", "")
            if not user_input:
                return {"response": "안녕하세요! 무엇을 도와드릴까요?"}
            
            # Gemini로 일반 응답 생성
            prompt = f"""
사용자의 질문에 친절하고 도움이 되는 답변을 해주세요.

사용자 질문: {user_input}

답변:
"""
            
            llm = get_gemini_model(temperature=0.7)
            response = llm.invoke(prompt)
            
            return {"response": response.content}

        def route_initial_request(state):
            """
            검사된 state를 기반으로 라우팅합니다.
            """
            # 'input' 키가 있는지 확인하고, 있다면 해당 딕셔너리를 사용합니다.
            # CLI를 통해 실행될 때, 입력은 'input' 키 아래에 중첩될 수 있습니다.
            input_data = state.get("input", state)
            
            # 사용자 입력 추출
            user_input = input_data.get("user_input", "")
            if not user_input:
                # 입력이 없으면 일반 응답
                return "general_response"
            
            # LLM 기반 의도 분류로 라우팅
            return route_based_on_intent(state)

        builder = StateGraph(self.state)
        
        # 노드 추가
        builder.add_node("entry_point_inspector", entry_point_inspector)
        
        # InstagramContentVerificationNode 인스턴스 생성 및 메서드 바인딩
        instagram_node = InstagramContentVerificationNode()
        builder.add_node("instagram_content_verification", instagram_node.execute)
        
        builder.add_node("general_response", general_response_node)
        
        # 진입점 및 라우팅 설정
        builder.set_entry_point("entry_point_inspector")
        builder.add_conditional_edges("entry_point_inspector", route_initial_request)
        builder.add_edge("instagram_content_verification", "__end__")
        builder.add_edge("general_response", "__end__")
        
        workflow = builder.compile()
        workflow.name = self.name
        return workflow


# 관리 Workflow 인스턴스 생성
management_workflow = ManagementWorkflow(ManagementState)

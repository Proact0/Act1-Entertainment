import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logging.getLogger().setLevel(logging.INFO)
from langgraph.graph import StateGraph

from agents.base_workflow import BaseWorkflow
from agents.management.modules.nodes import InstagramContentVerificationNode
from agents.management.modules.state import ManagementState


class ManagementWorkflow(BaseWorkflow):
    """
    콘텐츠 관리를 위한 Workflow 클래스

    이 클래스는 프로젝트, 팀, 리소스의 관리와 크리에이터 직업 성장을 위한 Workflow를 정의합니다.
    BaseWorkflow를 상속받아 기본 구조를 구현하고, ManagementState를 사용하여 상태를 관리합니다.
    MCP 서버를 통한 인스타그램 컨텐츠 검증, 정책 검색, 위험 요소 분석 기능을 포함합니다.
    """

    def __init__(self, state):
        super().__init__()
        self.state = state

    def build(self):
        """
        관리 Workflow 그래프 구축 메서드

        StateGraph를 사용하여 콘텐츠 관리를 위한 Workflow 그래프를 구축합니다.
        리소스 관리, 인스타그램 컨텐츠 검증, 정책 검색, 위험 요소 분석 노드를 포함하며,
        조건부 라우팅을 통해 요청 유형에 따라 적절한 노드로 분기합니다.

        Returns:
            CompiledStateGraph: 컴파일된 상태 그래프 객체
        """
        
        def entry_point_inspector(state):
            """
            그래프의 실제 진입점에서 state를 검사하기 위한 디버깅 함수.
            """
            print(f"--- DEBUG: ENTRY POINT STATE ---")
            print(state)
            print(f"---------------------------------")
            # 이 함수는 상태를 변경하지 않고 그대로 반환합니다.
            return state

        def route_initial_request(state):
            """
            검사된 state를 기반으로 라우팅합니다.
            """
            # 'input' 키가 있는지 확인하고, 있다면 해당 딕셔너리를 사용합니다.
            # CLI를 통해 실행될 때, 입력은 'input' 키 아래에 중첩될 수 있습니다.
            input_data = state.get("input", {})
            
            if "content_text" in input_data or "query" in input_data:
                # 유효한 입력이 있으면 검증 노드로 이동
                return "instagram_content_verification"
            
            # 그렇지 않으면 바로 종료
            return "__end__"

        builder = StateGraph(self.state)
        
        # 노드 추가
        builder.add_node("entry_point_inspector", entry_point_inspector)
        builder.add_node("instagram_content_verification", InstagramContentVerificationNode().execute)
        
        # 진입점 및 라우팅 설정
        builder.set_entry_point("entry_point_inspector")
        builder.add_conditional_edges("entry_point_inspector", route_initial_request)
        builder.add_edge("instagram_content_verification", "__end__")
        
        workflow = builder.compile()
        workflow.name = self.name
        return workflow


# 관리 Workflow 인스턴스 생성
management_workflow = ManagementWorkflow(ManagementState)

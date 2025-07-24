from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver

from agents.base_workflow import BaseWorkflow
from agents.main_state import MainState
from agents.management.workflow import management_workflow

# 컴파일된 관리 에이전트 워크플로우
management_agent = management_workflow.build()

class MainWorkflow(BaseWorkflow):
    """
    메인 Workflow 클래스

    이 클래스는 모든 Agentic Workflow를 바탕으로 주요 Workflow를 정의합니다.
    초기 입력을 받아 적절한 하위 워크플로우로 라우팅하는 역할을 합니다.
    """

    def __init__(self, state):
        """
        Args:
            state (StateGraph): Workflow에서 사용할 상태 클래스
        """
        super().__init__()
        self.state = state

    def build(self):
        """
        메인 Workflow 그래프 구축 메서드

        StateGraph를 사용하여 메인 Workflow 그래프를 구축합니다.
        'management_agent'를 직접 호출하여 입력을 전달하고,
        하위 워크플로우가 작업을 수행하도록 합니다.

        Returns:
            CompiledStateGraph: 컴파일된 상태 그래프 객체
        """
        builder = StateGraph(self.state)
        
        # management_agent를 직접 호출하여 입력을 전달
        builder.add_node("management_agent", management_agent)
        
        # 진입점을 management_agent로 설정
        builder.set_entry_point("management_agent")
        
        # management_agent 작업 완료 후 종료
        builder.add_edge("management_agent", END)
        
        # 메모리 내 체크포인트 설정
        memory = SqliteSaver.from_conn_string(":memory:")
        
        # 그래프 컴파일
        workflow = builder.compile(checkpointer=memory)
        workflow.name = self.name  # Workflow 이름 설정
        return workflow

# 메인 Workflow 인스턴스 생성
main_workflow = MainWorkflow(MainState)

from langgraph.graph import StateGraph

from agents.base_workflow import BaseWorkflow
from agents.management.modules.nodes import ResourceManagementNode
from agents.management.modules.state import ManagementState


class ManagementWorkflow(BaseWorkflow):
    """
    콘텐츠 관리를 위한 Workflow 클래스

    이 클래스는 프로젝트, 팀, 리소스의 관리와 크리에이터 직업 성장을 위한 Workflow를 정의합니다.
    BaseWorkflow를 상속받아 기본 구조를 구현하고, ManagementState를 사용하여 상태를 관리합니다.
    """

    def __init__(self, state):
        super().__init__()
        self.state = state

    def build(self):
        """
        관리 Workflow 그래프 구축 메서드

        StateGraph를 사용하여 콘텐츠 관리를 위한 Workflow 그래프를 구축합니다.
        현재는 리소스 관리 노드를 포함하고 있으며, 추후 조건부 에지를 추가하여
        다양한 경로를 가진 Workflow를 구축할 수 있습니다.

        Returns:
            CompiledStateGraph: 컴파일된 상태 그래프 객체
        """
        builder = StateGraph(self.state)
        # 리소스 관리 노드 추가
        builder.add_node("resource_management", ResourceManagementNode())
        # 시작 노드에서 리소스 관리 노드로 연결
        builder.add_edge("__start__", "resource_management")
        # 리소스 관리 노드에서 종료 노드로 연결
        builder.add_edge("resource_management", "__end__")

        # 조건부 에지 추가 예시
        # builder.add_conditional_edges(
        #     "resource_planning",
        #     # resource_planning 실행이 완료된 후, 다음 노드(들)는
        #     # router의 출력을 기반으로 예약됩니다
        #     router,
        # )

        workflow = builder.compile()  # 그래프 컴파일
        workflow.name = self.name  # Workflow 이름 설정

        return workflow


# 관리 Workflow 인스턴스 생성
management_workflow = ManagementWorkflow(ManagementState)

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
        builder = StateGraph(self.state)
        builder.add_node("instagram_content_verification", InstagramContentVerificationNode().execute)
        builder.add_edge("__start__", "instagram_content_verification")
        builder.add_edge("instagram_content_verification", "__end__")
        workflow = builder.compile()
        workflow.name = self.name
        return workflow


# 관리 Workflow 인스턴스 생성
management_workflow = ManagementWorkflow(ManagementState)

from langgraph.graph import StateGraph

from agents.base_workflow import BaseWorkflow
from agents.text.modules.nodes import (
    GenTextNode,
    PersonaExtractionNode,
    TextContentCheckNode,
    TextRegenerateRouterNode
,
)
from agents.text.modules.state import TextState


class TextWorkflow(BaseWorkflow):
    """
    텍스트 관련 콘텐츠 생성을 위한 Workflow 클래스

    이 클래스는 텍스트 기반 콘텐츠 생성을 위한 Workflow를 정의합니다.
    BaseWorkflow를 상속받아 기본 구조를 구현하고, TextState를 사용하여 상태를 관리합니다.
    """

    def __init__(self, state):
        super().__init__()
        self.state = state

    def build(self):
        """
        텍스트 Workflow 그래프 구축 메서드

        StateGraph를 사용하여 텍스트 처리를 위한 Workflow 그래프를 구축합니다.
        현재는 페르소나 추출 노드를 포함하고 있으며, 추후 조건부 에지를 추가하여
        다양한 경로를 가진 Workflow를 구축할 수 있습니다.

        Returns:
            CompiledStateGraph: 컴파일된 상태 그래프 객체
        """
        builder = StateGraph(self.state)
        # 페르소나 추출 노드 추가
        builder.add_node("persona_extraction", PersonaExtractionNode())

        # 텍스트 생성 노드 추가
        builder.add_node("text_generation", GenTextNode())

        # 텍스트 컨텐츠 체커 노드 추가
        builder.add_node("text_content_check", TextContentCheckNode())

        # 텍스트 재생성 노드 추가
        builder.add_node("text_regenerate_router", TextRegenerateRouterNode())

        # 시작 노드에서 페르소나 추출 노드로 연결
        builder.add_edge("__start__", "persona_extraction")
        # 페르소나 추출 노드에서 텍스트 생성 노드로 연결
        builder.add_edge("persona_extraction", "text_generation")
        # 텍스트 생성 노드에서 텍스트 컨텐츠 체커 노드로 연결
        builder.add_edge("text_generation", "text_content_check")
        # 텍스트 컨텐츠 체커 노드에서 텍스트 재생성 노드로 연결
        builder.add_edge("text_content_check", "text_regenerate_router")

        # 조건부 에지 추가
        builder.add_conditional_edges(
            "text_regenerate_router",
            lambda state: state["next"],  # state에서 next 키의 값을 사용
            {
                "text_generation": "text_content_check",  # 실패시 text_generation으로 돌아감
                "__end__": "__end__",  # 성공시 종료
            },
        )

        workflow = builder.compile()  # 그래프 컴파일
        workflow.name = self.name  # Workflow 이름 설정

        return workflow


# 텍스트 Workflow 인스턴스 생성
text_workflow = TextWorkflow(TextState)

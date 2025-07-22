"""
이미지 관련 콘텐츠 생성을 위한 Workflow 모듈

이 모듈은 이미지 기반 콘텐츠 생성을 위한 Workflow를 정의합니다.
StateGraph를 사용하여 이미지 처리를 위한 워크플로우를 구축합니다.
"""

from langgraph.graph import StateGraph

from agents.base_workflow import BaseWorkflow
from agents.image.modules.nodes import (
    concept_adapter_for_outfit_node,
    concept_adapter_for_pose_node,
    generate_outfit_prompt_node,
    generate_pose_prompt_node,
    generate_storyboard_node,
    refine_outfit_prompt_node,
    refine_outfit_prompt_with_llm_node,
    refine_pose_prompt_with_llm_node,
)
from agents.image.modules.state import ImageState


class ImageWorkflow(BaseWorkflow):
    """
    이미지 관련 콘텐츠 생성을 위한 Workflow 클래스

    이 클래스는 이미지 기반 콘텐츠 생성을 위한 Workflow를 정의합니다.
    BaseWorkflow를 상속받아 기본 구조를 구현하고, ImageState를 사용하여 상태를 관리합니다.
    """

    def __init__(self, state):
        super().__init__()
        self.state = state
        self.name = "image_workflow"  # ← 여기 추가

    def build(self):
        """
        이미지 Workflow 그래프 구축 메서드

        StateGraph를 사용하여 이미지 처리를 위한 Workflow 그래프를 구축합니다.
        현재는 간단한 구조로 시작 노드에서 종료 노드로 직접 연결되어 있으며,
        추후 이미지 생성 노드 등을 추가하여 확장할 수 있습니다.

        Returns:
            CompiledStateGraph: 컴파일된 상태 그래프 객체
        """
        builder = StateGraph(self.state)

        builder.add_node("generate_storyboard", generate_storyboard_node)
        # 의상 프롬프트 생성 노드 추가
        builder.add_node("adapt_outfit_concept", concept_adapter_for_outfit_node)
        builder.add_node("generate_outfit_prompt", generate_outfit_prompt_node)
        builder.add_node("refine_outfit_prompt_rule", refine_outfit_prompt_node)
        builder.add_node("refine_outfit_prompt_llm", refine_outfit_prompt_with_llm_node)

        # 포즈 프롬프트 생성 노드 추가
        builder.add_node("adapt_pose_concept", concept_adapter_for_pose_node)
        builder.add_node("generate_pose_prompt", generate_pose_prompt_node)
        builder.add_node("refine_pose_prompt_llm", refine_pose_prompt_with_llm_node)

        # Edge 설정
        builder.add_edge("__start__", "generate_storyboard")
        builder.add_edge("generate_storyboard", "adapt_outfit_concept")
        # builder.add_edge("__start__", "adapt_outfit_concept")
        # builder.add_edge("__start__", "adapt_pose_concept")

        # outfit
        builder.add_edge("adapt_outfit_concept", "generate_outfit_prompt")
        builder.add_edge("generate_outfit_prompt", "refine_outfit_prompt_rule")
        builder.add_edge("generate_outfit_prompt", "refine_outfit_prompt_llm")
        builder.add_edge("refine_outfit_prompt_rule", "__end__")
        builder.add_edge("refine_outfit_prompt_llm", "__end__")

        # pose
        builder.add_edge("adapt_pose_concept", "generate_pose_prompt")
        builder.add_edge("generate_pose_prompt", "refine_pose_prompt_llm")
        builder.add_edge("refine_pose_prompt_llm", "__end__")

        workflow = builder.compile()  # 그래프 컴파일
        workflow.name = self.name  # Workflow 이름 설정

        return workflow


# 이미지 Workflow 인스턴스 생성
image_workflow = ImageWorkflow(ImageState)

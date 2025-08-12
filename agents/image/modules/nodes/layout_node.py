"""
노드 클래스 모듈

해당 클래스 모듈은 각각 노드 클래스가 BaseNode를 상속받아 노드 클래스를 구현하는 모듈입니다.
"""

from agents.base_node import BaseNode

from agents.image.modules.chains import set_layout_choose_chain

class LayoutNode(BaseNode):
    """
    레이아웃 선택 노드

    이 노드는 앨범 커버 스타일에 적합한 레이아웃을 선택하는 기능을 담당합니다.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # BaseNode 초기화
        self.chain = set_layout_choose_chain()  # 레이아웃 선택 체인 설정

    def execute(self, state) -> dict:
        """
        주어진 상태(state)에서 앨범 커버 스타일과 concepts를 추출하여
        레이아웃 선택 체인에 전달하고, 결과를 응답으로 반환합니다.

        Args:
            state: 현재 워크플로우 상태

        Returns:
            dict: 선택된 개념들의 리스트가 포함된 응답
        """
        response = self.chain.invoke(
            {
                "output_storyboard": state["output_storyboard"],  # 출력 스토리보드
            }
        )
        return {
            "response": response,  # 응답 메시지
        }

SAMPLE_INPUT = {
  "main_theme": "감정의 여행",
  "story_summary": "밤하늘에 비친 달빛 아래, 불 켜진 창문이 있는 집이 보인다. 그 집 안에서는 따뜻한 빛이 넘쳐나고, 창밖으로는 색종이 조각들이 날아다니며 신난 분위기를 조성한다. 그리고 집 앞에 서 있는 인물은 핀 조명이 비추는 무대 위에서 열정적으로 노래를 부르며, 그 열정은 주변을 밝히고 있다. 이 장면은 그리움에서 활기로, 그리고 열정으로의 감정의 흐름을 연출한다.",
  "mood_tags": ["따뜻함", "그리움", "신남", "열정", "에너지"],
  "dominant_colors": ["#F5F5DC", "#FFFF00", "#FFA500"],
  "texture_keywords": ["나무", "반짝이는 글리터", "벨벳"],
  "visual_motifs": ["불 켜진 창문이 있는 집", "색종이 조각", "핀 조명"],
  "includes_human" : "true"
}
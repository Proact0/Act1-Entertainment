"""
노드 클래스 모듈

해당 클래스 모듈은 각각 노드 클래스가 BaseNode를 상속받아 노드 클래스를 구현하는 모듈입니다.
"""

from agents.base_node import BaseNode

from agents.image.modules.chains import set_concept_choose_chain

class ConceptChooseNode(BaseNode):
    """
    개념 선택 노드

    이 노드는 앨범 커버 스타일에 적합한 개념을 선택하는 기능을 담당합니다.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # BaseNode 초기화
        self.chain = set_concept_choose_chain()  # 개념 선택 체인 설정

    def execute(self, state) -> dict:
        """
        주어진 상태(state)에서 앨범 커버 스타일과 concepts를 추출하여
        개념 선택 체인에 전달하고, 결과를 응답으로 반환합니다.

        Args:
            state: 현재 워크플로우 상태

        Returns:
            dict: 선택된 개념들의 리스트가 포함된 응답
        """
        response = self.chain.invoke(
            {
                "album_cover_style": state["album_cover_style"],  # 앨범 커버 스타일
                "concepts": state["decomposition_concepts"],  # 제공된 개념들
            }
        )
        return {
            "chosen_concepts" : response
        }
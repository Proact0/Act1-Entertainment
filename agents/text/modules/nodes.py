"""
노드 클래스 모듈

해당 클래스 모듈은 각각 노드 클래스가 BaseNode를 상속받아 노드 클래스를 구현하는 모듈입니다.
"""

from agents.base_node import BaseNode
from agents.text.modules.chains import set_extraction_chain
from agents.text.modules.persona import PERSONA
from agents.text.modules.state import TextState


class PersonaExtractionNode(BaseNode):
    """
    콘텐츠 종류에 적합한 페르소나를 추출하는 노드
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # BaseNode 초기화
        self.chain = set_extraction_chain()  # 페르소나 추출 체인 설정

    def execute(self, state: TextState) -> dict:
        """
        주어진 상태(state)에서 핵심 키워드와 페르소나를 추출하여, 이미지 생성 노드에 전달합니다.
        """
        # 페르소나 추출 체인 실행
        extracted_persona = self.chain.invoke(
            {
                "content_topic": state["content_topic"],  # 콘텐츠 주제
                "content_type": state["content_type"],  # 콘텐츠 유형
                "persona_details": PERSONA,  # 페르소나 세부 정보
            }
        )

        state["persona_extracted"] = extracted_persona

        # 추출된 페르소나를 응답으로 반환
        return {"response": extracted_persona}
    
class getInputNode(BaseNode):
    """
    다른 노드로부터 온 input을 받는 노드 
    """

    

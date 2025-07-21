"""
노드 클래스 모듈

해당 클래스 모듈은 각각 노드 클래스가 BaseNode를 상속받아 노드 클래스를 구현하는 모듈입니다.

아래는 예시입니다.
"""

from agents.base_node import BaseNode
from agents.management.modules.chains import set_instagram_content_verification_chain
from agents.management.modules.state import ManagementState
import logging

class InstagramContentVerificationNode(BaseNode):
    """
    인스타그램 컨텐츠 검증만 수행하는 단일 노드
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chain = set_instagram_content_verification_chain

    async def execute(self, state: ManagementState) -> dict:
        logger = logging.getLogger(__name__)
        logger.info("[노드] InstagramContentVerificationNode.execute 호출")
        # state에서 content_text, content_type 추출
        content_text = state.get("content_text", "")
        content_type = state.get("content_type", "text")
        # 체인 실행
        result = await self.chain(content_text, content_type)
        state["content_verification_result"] = result
        return {"response": result}

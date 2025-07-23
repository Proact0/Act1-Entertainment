"""
노드 클래스 모듈

해당 클래스 모듈은 각각 노드 클래스가 BaseNode를 상속받아 노드 클래스를 구현하는 모듈입니다.

아래는 예시입니다.
"""

import asyncio
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
        print("노드 실행", state)
        logger = logging.getLogger(__name__)
        logger.info(f"[노드] InstagramContentVerificationNode.execute 비동기 호출 - state: {state}")

        # content_verification_result 내부까지 탐색
        content_verification = state.get("content_verification_result", {})
        content_text = (
            state.get("content_text")
            or state.get("query", "")
            or content_verification.get("content_text", "")
        )
        content_type = (
            state.get("content_type")
            or content_verification.get("content_type", "text")
        )
        logger.info(f"[노드] content_text: {content_text}, content_type: {content_type}")

        result = await self.chain(content_text, content_type)
        state["content_verification_result"] = result
        return {"response": result}

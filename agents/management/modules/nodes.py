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

    def execute(self, state: ManagementState) -> dict:
        print("노드 실행", state)
        logger = logging.getLogger(__name__)
        logger.info(f"[노드] InstagramContentVerificationNode.execute 호출 - state: {state}")

        # langgraph API는 입력을 'input' 키 아래에 중첩시킬 수 있습니다.
        # 'input' 키가 있는지 확인하고, 있다면 해당 딕셔너리를 사용합니다.
        input_data = state.get("input") if isinstance(state.get("input"), dict) else state

        content_verification = state.get("content_verification_result", {})
        
        content_text = (
            input_data.get("content_text")
            or input_data.get("query", "")
            or content_verification.get("content_text", "")
        )
        content_type = (
            input_data.get("content_type")
            or content_verification.get("content_type", "text")
        )
        logger.info(f"[노드] content_text: {content_text}, content_type: {content_type}")

        # self.chain이 함수이므로 직접 호출
        result = self.chain(content_text, content_type)
        state["content_verification_result"] = result
        return {"response": result}

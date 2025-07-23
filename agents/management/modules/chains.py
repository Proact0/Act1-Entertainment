"""LangChain 체인을 설정하는 함수 모듈

LCEL(LangChain Expression Language)을 사용하여 체인을 구성합니다.
기본적으로 modules.prompt 템플릿과 modules.models 모듈을 사용하여 LangChain 체인을 생성합니다.

"""

from typing import Any, Dict

from langchain.schema.runnable import RunnablePassthrough, RunnableSerializable
from langchain_core.output_parsers import StrOutputParser

from agents.management.modules.models import get_openai_model
from agents.management.modules.tools import verify_instagram_content_tool
import logging


async def set_instagram_content_verification_chain(
    content_text: str, content_type: str = "text"
) -> Dict[str, Any]:
    logger = logging.getLogger(__name__)
    logger.info(f"[체인] set_instagram_content_verification_chain 비동기 호출 - content_text: {content_text}, content_type: {content_type}")
    """
    인스타그램 컨텐츠 검증을 위한 체인을 생성합니다.

    Args:
        content_text: 검증할 컨텐츠 텍스트
        content_type: 컨텐츠 유형

    Returns:
        Dict[str, Any]: 검증 결과
    """
    return await verify_instagram_content_tool(content_text, content_type)

"""
도구(Tools) 모듈

이 모듈은 Management Workflow에서 사용할 수 있는 다양한 도구를 정의합니다.
도구는 LLM이 프로젝트 관리, 리소스 할당, 팀 관리 등을 지원하는 함수들입니다.

아래는 엔터테인먼트 프로젝트 관리에 적합한 도구의 예시입니다:
- 프로젝트 일정 관리 도구: 일정 생성, 수정, 추적
- 팀 구성원 할당 도구: 팀원 정보 검색 및 역할 할당
- 리소스 검색 도구: 가용 리소스 출력 및 할당 상태 확인
- 참조 자료 검색 도구: 엔터테인먼트 산업의 프로젝트 관리 사례 검색
- 협업 지원 도구: 팀원간 커뮤니케이션 및 협업 지원
- MCP 서버 도구: 인스타그램 컨텐츠 검증, 정책 검색, 위험 요소 분석
"""

from typing import Any, Dict
import logging
import asyncio

from agents.management.modules.mcp.mcp_client import verify_instagram_content


async def verify_instagram_content_tool(
    content_text: str, content_type: str = "text"
) -> Dict[str, Any]:
    logger = logging.getLogger(__name__)
    logger.info(f"[도구] verify_instagram_content_tool 비동기 호출 - content_text: {content_text}, content_type: {content_type}")
    try:
        result = await verify_instagram_content(content_text, content_type)
        return result
    except Exception as e:
        logger.error(f"[도구] 예외 발생: {e}")
        return {
            "error": f"인스타그램 컨텐츠 검증 중 오류 발생: {str(e)}",
            "is_approved": False,
            "score": 0.0,
            "reasons": ["검증 중 오류가 발생했습니다."],
            "warnings": [],
            "suggestions": ["다시 시도해주세요."],
            "risk_level": "medium",
            "content_type": content_type,
            "tags": [],
        }

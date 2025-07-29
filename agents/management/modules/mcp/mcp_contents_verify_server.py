import json
import logging
import os
import asyncio
import base64
from typing import Any, Dict

import httpx
from dotenv import load_dotenv
from fastmcp import FastMCP

import sys

# .env 파일에서 환경 변수 로드
load_dotenv()

# 로깅 설정: 모든 로그를 stderr로 보냅니다.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
MCP_CONTENTS_HOST = os.getenv("MCP_CONTENTS_HOST", "0.0.0.0")
MCP_CONTENTS_PORT = int(os.getenv("MCP_CONTENTS_PORT", 8200))
MCP_CONTENTS_TRANSPORT = os.getenv("MCP_CONTENTS_TRANSPORT", "http")
logger.info(f"PERPLEXITY_API_KEY: {os.getenv('PERPLEXITY_API_KEY')}")

contents_mcp = FastMCP(
    name="contents_verify",
    instructions=(
        "Act as an Instagram content verification assistant that checks if content "
        "is appropriate for Instagram posting using real-time web search."
    ),
    host=MCP_CONTENTS_HOST,
    port=MCP_CONTENTS_PORT,
)


@contents_mcp.tool()
async def verify_instagram_content(
    content_text: str, content_type: str = "text"
) -> Dict[str, Any]:
    logger.info(f"[MCP 서버] verify_instagram_content 호출 - content_text: {content_text}, content_type: {content_type}")
    """
    Perplexity API를 사용하여 인스타그램 컨텐츠의 적절성을 실시간 웹 검색으로 검증합니다.
    """
    logger.info(f"인스타그램 컨텐츠 검증 시작: {content_type}")
    logger.info(f"컨텐츠 길이: {len(content_text)} 문자")
    logger.info(f"verify_instagram_content called with: {content_text}, {content_type}")

    if not content_text or not content_text.strip():
        return {
            "error": "컨텐츠 텍스트가 비어 있습니다.",
            "is_approved": False,
            "score": 0.0,
            "reasons": ["검증할 컨텐츠가 없습니다."],
            "warnings": [],
            "suggestions": ["컨텐츠를 입력해주세요."],
            "risk_level": "high",
            "content_type": content_type,
            "tags": [],
        }

    if not PERPLEXITY_API_KEY:
        return {
            "error": "PERPLEXITY_API_KEY가 설정되지 않았습니다.",
            "is_approved": False,
            "score": 0.0,
            "reasons": ["API 키가 없어 검증을 수행할 수 없습니다."],
            "warnings": [],
            "suggestions": ["PERPLEXITY_API_KEY를 설정해주세요."],
            "risk_level": "high",
            "content_type": content_type,
            "tags": [],
        }

    try:
        # Perplexity API를 통한 인스타그램 정책 검색 및 컨텐츠 검증
        prompt = f"""
다음 인스타그램 컨텐츠를 검증해주세요:

컨텐츠 유형: {content_type}
컨텐츠 텍스트: {content_text}

실시간 웹 검색을 통해 다음을 확인해주세요:
1. 인스타그램 커뮤니티 가이드라인 및 정책
2. 유사한 컨텐츠의 위반 사례
3. 현재 인스타그램에서 금지하는 키워드나 주제
4. 최근 인스타그램 정책 변경사항
5. 해당 컨텐츠의 잠재적 위험 요소

검색 키워드 예시:
- "Instagram community guidelines 2024"
- "Instagram content policy violations"
- "Instagram banned content examples"
- "Instagram content moderation rules"

다음 JSON 형태로 결과를 반환해주세요:
{{
    "is_approved": true/false,
    "score": 0.0-1.0,
    "reasons": ["승인/거부 이유들 (웹 검색 결과 기반)"],
    "warnings": ["경고사항들"],
    "suggestions": ["개선 제안사항들"],
    "risk_level": "low/medium/high",
    "policy_references": ["참조한 정책들"],
    "similar_cases": ["유사한 사례들"],
    "tags": ["관련 태그들"]
}}
"""

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "sonar",
                    "messages": [
                        {"role": "user", "content": prompt},
                    ],
                },
            )

            if response.status_code != 200:
                # API 에러 발생 시, 응답 본문을 로깅하여 더 자세한 정보를 확인합니다.
                error_details = response.text
                logger.error(f"Perplexity API 오류: {response.status_code} - {error_details}")
                raise Exception(f"Perplexity API 오류: {response.status_code}")

            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # Perplexity API 응답 로깅
            logger.info(f"Perplexity API 응답 상태: {response.status_code}")
            logger.info(f"Perplexity API 원본 응답: {content}")
            
            # JSON 파싱
            try:
                parsed_result = json.loads(content)
                logger.info(f"Perplexity API 파싱된 결과: {json.dumps(parsed_result, ensure_ascii=False, indent=2)}")
                final_result = {
                    "is_approved": parsed_result.get("is_approved", False),
                    "score": float(parsed_result.get("score", 0.0)),
                    "reasons": parsed_result.get("reasons", []),
                    "warnings": parsed_result.get("warnings", []),
                    "suggestions": parsed_result.get("suggestions", []),
                    "risk_level": parsed_result.get("risk_level", "medium"),
                    "content_type": content_type,
                    "policy_references": parsed_result.get("policy_references", []),
                    "similar_cases": parsed_result.get("similar_cases", []),
                    "tags": parsed_result.get("tags", []),
                }
                
                logger.info(f"최종 검증 결과: {json.dumps(final_result, ensure_ascii=False, indent=2)}")
                return final_result
            except json.JSONDecodeError:
                return {
                    "error": "Perplexity API 응답 파싱 실패",
                    "is_approved": False,
                    "score": 0.0,
                    "reasons": ["Perplexity API 응답이 올바른 JSON이 아닙니다."],
                    "warnings": [],
                    "suggestions": ["다시 시도해주세요."],
                    "risk_level": "medium",
                    "content_type": content_type,
                    "tags": [],
                }

    except httpx.ReadTimeout:
        logger.error("Perplexity API 응답 시간 초과")
        return {
            "error": "Perplexity API 응답 시간 초과",
            "is_approved": False,
            "score": 0.0,
            "reasons": ["Perplexity API에서 응답이 지연되어 검증을 완료할 수 없습니다."],
            "warnings": ["네트워크 상태나 Perplexity API의 부하 문제일 수 있습니다."],
            "suggestions": ["잠시 후 다시 시도해주세요."],
            "risk_level": "medium",
            "content_type": content_type,
            "tags": [],
        }
    except Exception as e:
        # 예외 발생 시, 예외 유형과 메시지, 표현을 모두 로깅합니다.
        logger.error(f"검증 중 예외 발생: {type(e).__name__} - {e!r}")
        return {
            "error": f"검증 중 오류 발생: {type(e).__name__}",
            "is_approved": False,
            "score": 0.0,
            "reasons": ["검증 중 오류가 발생했습니다."],
            "warnings": [],
            "suggestions": ["다시 시도해주세요."],
            "risk_level": "medium",
            "content_type": content_type,
            "tags": [],
        }


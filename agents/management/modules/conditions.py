"""
조건부 라우팅을 위한 모듈

LLM을 사용해서 사용자 의도를 분류하고 적절한 노드로 라우팅합니다.
"""

import json
import logging
from agents.management.modules.models import get_gemini_model

logger = logging.getLogger(__name__)

def classify_user_intent(user_input: str):
    """
    Gemini LLM을 사용해서 사용자 의도를 분류
    
    Args:
        user_input (str): 사용자 입력
        
    Returns:
        dict: {"intent": "content_verification|other", "confidence": 0.0-1.0}
    """
    try:
        prompt = f"""
사용자 입력을 분석해서 어떤 작업인지 판단해주세요.

사용자 입력: {user_input}

가능한 작업:
1. content_verification: 인스타그램 컨텐츠 검증 요청
   - "검증해줘", "검사해줘", "위험한가", "적절한가" 등의 키워드
   - 특정 텍스트나 컨텐츠에 대한 검증 요청
2. other: 일반적인 질문이나 다른 작업

JSON 형태로만 응답해주세요:
{{"intent": "content_verification|other", "confidence": 0.0-1.0, "reason": "판단 이유"}}
"""

        llm = get_gemini_model(temperature=0.1)
        response = llm.invoke(prompt)
        
        # 디버깅: LLM 응답 확인
        logger.info(f"LLM 원본 응답: {response.content}")
        
        # JSON 파싱 (마크다운 코드 블록 처리 포함)
        try:
            content = response.content.strip()
            
            # 마크다운 코드 블록 제거
            if content.startswith("```json"):
                content = content[7:]  # "```json" 제거
            if content.startswith("```"):
                content = content[3:]   # "```" 제거
            if content.endswith("```"):
                content = content[:-3]  # 끝의 "```" 제거
            
            content = content.strip()
            result = json.loads(content)
            logger.info(f"의도 분류 결과: {result}")
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON 파싱 오류: {e}")
            logger.error(f"파싱 실패한 응답: {response.content}")
            # JSON이 아닌 경우 기본값 반환
            return {
                "intent": "other",
                "confidence": 0.0,
                "reason": "JSON 파싱 실패"
            }
        
        return result
        
    except Exception as e:
        logger.error(f"의도 분류 중 오류 발생: {e}")
        # 오류 시 기본값 반환
        return {
            "intent": "other",
            "confidence": 0.0,
            "reason": "분류 중 오류 발생"
        }

def route_based_on_intent(state):
    """
    LLM이 사용자 의도를 판단해서 적절한 노드로 라우팅
    
    Args:
        state: 현재 상태
        
    Returns:
        str: 다음 노드 이름
    """
    # 사용자 입력 추출
    user_input = state.get("user_input", "")
    if not user_input:
        # 입력이 없으면 일반 응답
        return "general_response"
    
    # LLM으로 의도 분류
    intent_result = classify_user_intent(user_input)
    
    logger.info(f"라우팅 결정: {intent_result}")
    
    # 컨텐츠 검증 의도이고 확신도가 높으면 검증 노드로
    if (intent_result["intent"] == "content_verification" and 
        intent_result["confidence"] > 0.7):
        return "instagram_content_verification"
    else:
        return "general_response"

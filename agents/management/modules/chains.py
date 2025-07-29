"""LangChain 체인을 설정하는 함수 모듈

LCEL(LangChain Expression Language)을 사용하여 체인을 구성합니다.
modules.prompts, modules.models, modules.conditions를 모두 활용하여 
통합된 LangChain 체인을 생성합니다.

"""

from typing import Any, Dict
import json
import logging

from langchain.schema.runnable import RunnablePassthrough, RunnableSerializable
from langchain_core.output_parsers import StrOutputParser

from agents.management.modules.models import get_gemini_model
from agents.management.modules.prompts import get_content_verification_prompt
from agents.management.modules.conditions import classify_user_intent
from agents.management.modules.tools import verify_instagram_content_tool

logger = logging.getLogger(__name__)

def create_intent_classification_chain():
    """
    사용자 의도를 분류하는 체인을 생성합니다.
    
    Returns:
        RunnableSerializable: 의도 분류 체인
    """
    def classify_intent(input_data: Dict[str, Any]) -> Dict[str, Any]:
        user_input = input_data.get("user_input", "")
        intent_result = classify_user_intent(user_input)
        return {
            **input_data,
            "intent_result": intent_result
        }
    
    return classify_intent

def create_content_verification_chain():
    """
    컨텐츠 검증을 수행하는 체인을 생성합니다.
    
    Returns:
        RunnableSerializable: 컨텐츠 검증 체인
    """
    def verify_content(input_data: Dict[str, Any]) -> Dict[str, Any]:
        user_input = input_data.get("user_input", "")
        
        # 사용자 입력에서 검증할 텍스트 추출
        # 예: "오나전 야마를 검증해줘" -> "오나전 야마"
        extraction_prompt = f"""
사용자 입력에서 검증할 텍스트를 추출해주세요.

사용자 입력: {user_input}

JSON 형태로 응답해주세요:
{{"content_text": "추출된 텍스트", "content_type": "text"}}
"""
        
        llm = get_gemini_model(temperature=0.1)
        extraction_result = llm.invoke(extraction_prompt)
        
        try:
            extracted = json.loads(extraction_result.content)
            content_text = extracted.get("content_text", user_input)
            content_type = extracted.get("content_type", "text")
        except:
            content_text = user_input
            content_type = "text"
        
        # MCP 서버를 통한 검증 수행
        verification_result = verify_instagram_content_tool(content_text, content_type)
        
        return {
            **input_data,
            "verification_result": verification_result,
            "content_text": content_text,
            "content_type": content_type
        }
    
    return verify_content

def create_result_analysis_chain():
    """
    검증 결과를 분석하고 요약하는 체인을 생성합니다.
    
    Returns:
        RunnableSerializable: 결과 분석 체인
    """
    prompt = get_content_verification_prompt()
    llm = get_gemini_model(temperature=0.3)
    
    chain = prompt | llm | StrOutputParser()
    
    def analyze_result(input_data: Dict[str, Any]) -> Dict[str, Any]:
        verification_result = input_data.get("verification_result", {})
        
        # 검증 결과를 문자열로 변환
        if isinstance(verification_result, dict):
            result_str = json.dumps(verification_result, ensure_ascii=False, indent=2)
        else:
            result_str = str(verification_result)
        
        # LLM으로 결과 분석
        analysis = chain.invoke({"verification_result": result_str})
        
        return {
            **input_data,
            "analysis": analysis
        }
    
    return analyze_result

def create_general_response_chain():
    """
    일반적인 질문에 대한 응답 체인을 생성합니다.
    
    Returns:
        RunnableSerializable: 일반 응답 체인
    """
    def generate_response(input_data: Dict[str, Any]) -> Dict[str, Any]:
        user_input = input_data.get("user_input", "")
        
        prompt = f"""
사용자의 질문에 친절하고 도움이 되는 답변을 한국어로 해주세요.

사용자 질문: {user_input}

답변:
"""
        
        llm = get_gemini_model(temperature=0.7)
        response = llm.invoke(prompt)
        
        return {
            **input_data,
            "response": response.content
        }
    
    return generate_response

def set_instagram_content_verification_chain(
    content_text: str, content_type: str = "text"
) -> Dict[str, Any]:
    """
    인스타그램 컨텐츠 검증을 위한 체인을 생성합니다.
    (기존 호환성을 위한 함수)

    Args:
        content_text: 검증할 컨텐츠 텍스트
        content_type: 컨텐츠 유형

    Returns:
        Dict[str, Any]: 검증 결과
    """
    logger.info(f"[체인] set_instagram_content_verification_chain 호출 - content_text: {content_text}, content_type: {content_type}")
    
    # 1단계: MCP 서버를 통한 검증
    verification_result = verify_instagram_content_tool(content_text, content_type)
    
    # 2단계: 검증 결과 분석
    analysis_chain = create_result_analysis_chain()
    result = analysis_chain({
        "verification_result": verification_result,
        "content_text": content_text,
        "content_type": content_type
    })
    
    return {
        "verification_result": verification_result,
        "analysis": result.get("analysis", ""),
        "content_text": content_text,
        "content_type": content_type
    }

def create_management_workflow_chain():
    """
    전체 관리 워크플로우를 위한 통합 체인을 생성합니다.
    
    Returns:
        RunnableSerializable: 통합 워크플로우 체인
    """
    def workflow_chain(input_data: Dict[str, Any]) -> Dict[str, Any]:
        user_input = input_data.get("user_input", "")
        
        if not user_input:
            return {"response": "안녕하세요! 무엇을 도와드릴까요?"}
        
        # 1단계: 의도 분류
        intent_chain = create_intent_classification_chain()
        intent_result = intent_chain.invoke(input_data)
        
        intent = intent_result.get("intent_result", {}).get("intent", "other")
        confidence = intent_result.get("intent_result", {}).get("confidence", 0.0)
        
        logger.info(f"의도 분류 결과: {intent}, 확신도: {confidence}")
        
        # 2단계: 의도에 따른 분기
        if intent == "content_verification" and confidence > 0.7:
            # 컨텐츠 검증 체인 실행
            verification_chain = create_content_verification_chain()
            verification_result = verification_chain.invoke(input_data)
            
            # 결과 분석 체인 실행
            analysis_chain = create_result_analysis_chain()
            final_result = analysis_chain.invoke(verification_result)
            
            return {
                "type": "content_verification",
                "verification_result": final_result.get("verification_result"),
                "analysis": final_result.get("analysis"),
                "content_text": final_result.get("content_text"),
                "content_type": final_result.get("content_type")
            }
        else:
            # 일반 응답 체인 실행
            response_chain = create_general_response_chain()
            response_result = response_chain.invoke(input_data)
            
            return {
                "type": "general_response",
                "response": response_result.get("response")
            }
    
    return workflow_chain

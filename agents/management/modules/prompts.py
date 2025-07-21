"""프롬프트 템플릿을 생성하는 함수 모듈

프롬프트 템플릿을 생성하는 함수 모듈을 구성합니다.
기본적으로 PromptTemplate를 사용하여 프롬프트 템플릿을 생성하고 반환합니다.

아래는 예시입니다.
"""

from langchain_core.prompts import PromptTemplate


def get_content_verification_prompt():
    """
    컨텐츠 검증 결과를 분석하는 프롬프트 템플릿을 생성합니다.

    Returns:
        PromptTemplate: 컨텐츠 검증 분석을 위한 프롬프트 템플릿 객체
    """
    content_verification_template = """당신은 엔터테인먼트 컨텐츠 관리 전문가입니다.\n\n다음 컨텐츠 검증 결과를 분석하고 한국어로 요약해주세요:\n\n검증 결과: {verification_result}\n\n다음 항목들을 포함하여 분석해주세요:\n1. 검증 결과 요약\n2. 주요 위험 요소\n3. 개선 제안사항\n4. 권장 조치사항\n\n분석 결과:"""
    return PromptTemplate(
        template=content_verification_template,
        input_variables=["verification_result"],
    )

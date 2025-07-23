"""LangChain 체인을 설정하는 함수 모듈

LCEL(LangChain Expression Language)을 사용하여 체인을 구성합니다.
기본적으로 modules.prompt 템플릿과 modules.models 모듈을 사용하여 LangChain 체인을 생성합니다.
"""

from langchain.schema.runnable import RunnablePassthrough, RunnableSerializable
from langchain_core.output_parsers import PydanticOutputParser

from agents.image.modules.models import get_gemini_model
from agents.image.modules.prompts import choose_concept_prompt

from typing import Literal, List
from pydantic import BaseModel, Field

class ConceptChosenOutput(BaseModel):
    """개념 선택 결과를 나타내는 모델"""
    concepts: List[dict] = Field(
        ..., description="앨범 커버 스타일에 적합한 개념들의 dictionary 리스트"
    )


def set_concept_choose_chain() -> RunnableSerializable:
    """
    개념 선택에 사용할 LangChain 체인을 생성합니다.

    체인은 다음 단계로 구성됩니다:
    1. 입력에서 앨범커버 스타일과 concepts를 추출하여 프롬프트에 전달
    2. 프롬프트 템플릿에 값을 삽입하여 최종 프롬프트 생성
    3. LLM을 호출하여 개념 선택 수행
    4. 결과를 문자열로 변환

    이 함수는 ConceptChooseNode에서 사용됩니다.

    Returns:
        RunnableSerializable: 실행 가능한 체인 객체
    """
    # 개념 선택을 위한 프롬프트 가져오기

    pydantic_parser = PydanticOutputParser(pydantic_object=ConceptChosenOutput)
    format_instructions = pydantic_parser.get_format_instructions()

    prompt = choose_concept_prompt()

    # Gemini 모델 가져오기
    model = get_gemini_model()

    # LCEL을 사용하여 체인 구성
    return (
        # 입력에서 필요한 필드 추출 및 프롬프트에 전달
        RunnablePassthrough.assign(
            album_cover_style=lambda x: x["album_cover_style"],  # 앨범 커버 스타일 추출
            concepts=lambda x: x["concepts"],  # 제공된 개념들 추출
            format_instructions=lambda x: format_instructions,  # 포맷 지침 전달
        )
        | prompt  # 프롬프트 적용
        | model   # LLM 모델 호출
        | PydanticOutputParser(pydantic_object=ConceptChosenOutput)  # 결과를 Pydantic 모델로 변환
    )


# def set_image_generation_chain() -> RunnableSerializable:
#     """
#     이미지 생성에 사용할 LangChain 체인을 생성합니다.
#
#     체인은 다음 단계로 구성됩니다:
#     1. 입력에서 query를 추출하여 프롬프트에 전달
#     2. 프롬프트 템플릿에 값을 삽입하여 최종 프롬프트 생성
#     3. LLM을 호출하여 이미지 생성 수행
#     4. 결과를 문자열로 변환
#
#     이 함수는 이미지 생성 노드에서 사용됩니다.
#
#     Returns:
#         RunnableSerializable: 실행 가능한 체인 객체
#     """
#     # 이미지 생성을 위한 프롬프트 가져오기
#     prompt = get_image_generation_prompt()
#     # OpenAI 모델 가져오기
#     model = get_openai_model()
#
#     # LCEL을 사용하여 체인 구성
#     return (
#         # 입력에서 필요한 필드 추출 및 프롬프트에 전달
#         RunnablePassthrough.assign(
#             query=lambda x: x["query"],  # 사용자 쿼리 추출
#         )
#         | prompt  # 프롬프트 적용
#         | model   # LLM 모델 호출
#         | StrOutputParser()  # 결과를 문자열로 변환
#     )

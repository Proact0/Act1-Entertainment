"""프롬프트 템플릿을 생성하는 함수 모듈

프롬프트 템플릿을 생성하는 함수 모듈을 구성합니다.
기본적으로 PromptTemplate을 사용하여 프롬프트 템플릿을 생성하고 반환합니다.
"""

from langchain_core.prompts import PromptTemplate
from agents.image.modules.state import ImageState

# def get_image_generation_prompt() -> str:
#     """
#     이미지 생성을 위한 프롬프트 템플릿을 반환합니다.

#     Returns:
#         str: 이미지 생성 프롬프트 템플릿
#     """
#     return """
#     목적: {purpose}
    
#     다음 텍스트를 기반으로 이미지를 생성해주세요:
#     {text}
    
#     이미지는 고품질이어야 하며, 텍스트의 감성과 분위기를 잘 표현해야 합니다.
#     """

def get_text_response_prompt(state: ImageState) -> str:
    """
    텍스트 응답 생성을 위한 프롬프트 템플릿을 반환합니다.

    Returns:
        str: 텍스트 응답 프롬프트 템플릿
    """
    return """
    목적: {content_type}
    
    다음 텍스트에 대한 이미지를 생성하고 있습니다:
    {content_topic}
    
    이 텍스트의 시각적 요소와 감성을 분석하고, 어떤 이미지가 생성될 것인지 설명해주세요.
    다음 요소들을 포함해서 설명해주세요:
    1. 주요 시각적 요소
    2. 색감과 톤
    3. 분위기와 감성
    4. 구도와 강조점
    """

def get_image_generation_prompt()->PromptTemplate:
    """
    이미지 생성을 위한 프롬프트 템플릿을 생성합니다.

    프롬프트는 LLM에게 사용자 쿼리에 맞는 이미지 생성 방법과
    이미지 특성을 설명하도록 지시합니다. 생성된 이미지 설명은 한국어로 반환됩니다.
    
    Returns:
        PromptTemplate: 이미지 생성을 위한 프롬프트 템플릿 객체
    """
    # 이미지 생성을 위한 프롬프트 템플릿 정의
    image_generation_template = """당신은 상업용 이미지 배경 디자이너 입니다.
        제가 드리는 페르소나와 내용에 따라서 배경 이미지 설명을 생성해 주세요.
        이미지에는 텍스트, 인물이 절대 들어가서는 안됩니다.
        여기에 부여되어야 하는 페르소나는 다음과 같습니다: {persona}
        이미지의 구성은 다음과 같습니다:
        이미지 유형 : {content_type}
        이미지 주제 : {content_topic}
        이미지 내용 : {context_detail}
      
    """

    # PromptTemplate 객체 생성 및 반환
    return PromptTemplate(
        template=image_generation_template,  # 정의된 프롬프트 템플릿
        input_variables=["content_type", "persona", "content_topic","context_detail"],  # 프롬프트에 삽입될 변수들
    )


def get_context_prompt()->PromptTemplate:
    """
    input으로 받은 json 객체를 해석할 수 있도록 하는 프롬프트 템플릿을 생성합니다.

    프롬프트는 input으로 받은 객체를 자신만의 언어로 다시 해석하도록 하는 내용을 담고 있습니다. 
    생성된 내용은 한국어로 반환됩니다.
    
    Returns:
        PromptTemplate: 이미지 생성을 위한 프롬프트 템플릿 객체
    
    
    """
    
    context_generation_template = """
    당신은 상업용 사진 감독 입니다. 제가 드리는 컨셉 키워드 들을 가지고 어떤 컨셉으로 사진을 촬영할지 지정해 주세요.
    제가 드리는 키워드는 이렇습니다 : {context}
    """

    return PromptTemplate(
        template = context_generation_template,
        input_variables = ["context"]
    )

"""프롬프트 템플릿을 생성하는 함수 모듈

프롬프트 템플릿을 생성하는 함수 모듈을 구성합니다.
기본적으로 PromptTemplate을 사용하여 프롬프트 템플릿을 생성하고 반환합니다.
"""

from langchain_core.prompts import PromptTemplate

def choose_concept_prompt():
    """분해된 콘셉트를 선택하기 위한 프롬프트 템플릿을 생성합니다.
    """
    template = """당신은 신곡의 앨범 커버를 기획하기 위해 구성된 컨셉들 중 제공되는 앨범 커버 스타일에 가장 적합한 것을 선택해야합니다.
도출 요구
- 앨범 커버 스타일: {album_cover_style}
- 제공된 컨셉들: {concepts}

당신은 다음과 같은 기준을 사용하여 가장 적합한 컨셉을 선택해야 합니다:
- 앨범 커버 스타일과의 일치성
- 컨셉의 독창성
- 컨셉의 시각적 매력
- 컨셉의 실행 가능성
- 컨셉의 대중성
- 컨셉의 트렌드 반영
- 컨셉의 감정적 연결
---
Output:
{format_instructions}

"""
    return PromptTemplate(
        template=template,
        input_variables=["album_cover_style", "concepts", "format_instructions"],
    )
    

# def get_image_generation_prompt():
#     """
#     이미지 생성을 위한 프롬프트 템플릿을 생성합니다.
#
#     프롬프트는 LLM에게 사용자 쿼리에 맞는 이미지 생성 방법과
#     이미지 특성을 설명하도록 지시합니다. 생성된 이미지 설명은 한국어로 반환됩니다.
#
#     Returns:
#         PromptTemplate: 이미지 생성을 위한 프롬프트 템플릿 객체
#     """
#     # 이미지 생성을 위한 프롬프트 템플릿 정의
#     image_generation_template = """당신은 이미지 생성 전문가로서 다양한 스타일과 주제의 이미지를 설명하고
# 생성하는 데 전문성을 가지고 있습니다. 다음 정보를 바탕으로 이미지를 생성해 주세요:

# 사용자 요청: {query}

# 작업:
# 위 입력을 사용하여 사용자의 요청에 맞는 이미지를 생성하고 설명해 주세요. 설명에는 다음 내용을 포함해야 합니다:

# - 이미지의 주요 요소와 구성
# - 이미지의 스타일과 분위기
# - 색상 팔레트와 조명 효과
# - 이미지가 전달하는 감정과 메시지

# 설명은 구체적이고 상세하게 작성하여 이미지 제작자가 이해하고 구현할 수 있도록 해주세요.
# 모든 응답은 한국어로 작성해 주세요.

# 생성된 이미지 설명:"""
#
#     # PromptTemplate 객체 생성 및 반환
#     return PromptTemplate(
#         template=image_generation_template,  # 정의된 프롬프트 템플릿
#         input_variables=["query"],  # 프롬프트에 삽입될 변수들
#     )

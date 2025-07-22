"""프롬프트 템플릿을 생성하는 함수 모듈

프롬프트 템플릿을 생성하는 함수 모듈을 구성합니다.
기본적으로 PromptTemplate을 사용하여 프롬프트 템플릿을 생성하고 반환합니다.
"""

from langchain_core.prompts import PromptTemplate

outfit_prompt_template = PromptTemplate.from_template(
    "You are a fashion styling expert. The user's request is: '{user_request}'.\n"
    "Please describe an outfit suitable for the season, location, and mood in detail.\n"
    "At the end of your response, include a section titled 'Image Generation Prompt:' and write one paragraph in English that describes only the clothing and accessories.\n"
    "Do not include background, facial expression, pose, or any scene-related details.\n"
    "Focus only on the fashion items — their style, color, texture, and how they are combined."
)

pose_prompt_template = PromptTemplate.from_template(
    "You are an expert in character expression and pose design.\n"
    "The following concept should be visually interpreted: '{user_request}'\n\n"
    "Your task is to write one concise, vivid English sentence that describes only the person's pose and facial expression.\n"
    "- Include facial emotion, gaze direction, hand gestures, body posture, and movement.\n"
    "- Do not mention clothing, background, or scene elements.\n"
    "- The sentence should be suitable for an image generation model.\n"
    "- Avoid generic expressions and ensure physical cues are clearly described."
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

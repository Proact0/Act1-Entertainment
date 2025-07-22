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


storyboard_prompt_template = PromptTemplate.from_template(
    "당신은 뮤직 앨범 아트 디렉터입니다. 다음은 앨범 커버 제작을 위한 핵심 콘셉트입니다:\n\n"
    "{concepts}\n\n"
    "이 정보를 바탕으로, **앨범 커버에 담길 장면**을 다음 조건에 맞춰 한 문단으로 서술하세요:\n"
    "1. 구체적인 시각적 이미지로 묘사된 장면일 것 (예: 시간대, 장소, 조명, 인물의 동작 등)\n"
    "2. 감정의 흐름이 느껴지도록 연출할 것 (예: 그리움에서 활기로 전환되는 느낌)\n"
    "3. '조화', '상징' 같은 추상적 단어보다는 시각적으로 떠올릴 수 있는 문장을 쓸 것\n"
    "4. 한국어로 작성할 것\n"
    "5. 제목처럼 한 줄로 전체 주제를 요약한 `main_theme`를 함께 생성할 것\n"
    "출력은 아래 JSON 형식을 따르며, 각 항목은 다음과 같은 의미를 가집니다:\n\n"
    "- main_theme: 전체를 관통하는 핵심 주제 (짧은 문장)\n"
    "- story_summary: 1문단 정도의 이야기적 흐름 (자연스러운 문장)\n"
    "- mood_tags: 대표 감정 또는 분위기 키워드 리스트\n"
    "- dominant_colors: 주요 색상 HEX 코드 리스트 (예: #FFA500)\n"
    "- texture_keywords: 시각적 질감 키워드 리스트 (예: 벨벳, 거친 표면 등)\n"
    "- visual_motifs: 공통된 시각적 오브젝트 또는 상징물 리스트\n\n"
    "- includes_human: 이미지에 인물이 등장하는지 여부 (true 또는 false)"
    "모든 출력은 한국어로 작성하고, 반드시 JSON 형식만 출력하세요.\n"
    "Output must be a valid JSON object only. Do NOT include ``` or any Markdown formatting."
)

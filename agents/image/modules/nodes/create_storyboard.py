from agents.base_node import BaseNode
from agents.image.modules.models import get_gemini_model

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

class CreateStoryboardNode(BaseNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prompt = self._create_prompt()
        self.chain = self._create_chain()

    def execute(self, state) -> dict:
        response = self.chain.invoke(
            {
                "concepts": state.get("chosen_concepts")
            }
        )

        return {
            "output_storyboard" : response
        }
    
    def _create_prompt(self):
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

        return storyboard_prompt_template

    def _create_chain(self):
        model = get_gemini_model()

        chain = self.prompt | model | JsonOutputParser()

        return chain
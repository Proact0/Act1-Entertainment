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


def choose_layout_prompt():
    """감정 흐름이 담긴 이미지 시나리오(output_storyboard)에 적합한 카메라 구도(각, 비율, 프레이밍)를 선택하기 위한 프롬프트 템플릿을 생성합니다.
    """
    template = """당신은 시각 이미지 제작 전문가입니다. 아래에 주어진 이미지 시나리오를 바탕으로, 가장 적합한 레이아웃 구도(카메라 각도, 화면 비율, 프레이밍)를 선택해야 합니다.

도출 요구:
- 이미지 시나리오: {output_storyboard}

당신은 다음의 기준을 고려하여 가장 적절한 레이아웃 구도를 판단해야 합니다:
- 장면의 감정적 흐름(예: 그리움 → 활기 → 열정)을 얼마나 잘 전달할 수 있는가
- 인물과 배경 사이의 관계를 효과적으로 시각화할 수 있는가
- 시네마틱한 매력과 시각적 임팩트를 제공하는가
- 트렌디하고 현대적인 연출이 가능한가
- 실제 연출(예: AI 이미지 생성 등)로 구현 가능한 구도인가

---
Output:
{format_instructions}
"""
    return PromptTemplate(
        template=template,
        input_variables=["output_storyboard", "format_instructions"],
    )

def decomposition_concept():
    prompt = """
GOAL:
신곡의 앨범 커버를 기획하기 위해
가사‧메시지‧노래 스타일을 ‘콘셉트 분해’작업을 진행해 주세요.

🎯 도출 요구
1. 키워드(가사과 스타일), 감정 및 분위기 매핑
2. 감정별 시각적 메타포/오브젝트 제안(예: 네온사인, 골드 컨페티)
3. 어울리는 색상과 질감 아이디어(HEX 코드 포함)  

📌 작성 규칙
- 키워드는 최소 6개 이상(핵심 키워드 다양화)  
- 메타포는 추상(예: “따뜻함”)이 아닌 구체 오브젝트로 표현  
- 장황한 설명 없이 출력
- 결과를 아래 JSON List 형식으로 처리
    conceptAnalyzer={json_schema}
    Return a `list[conceptAnalyzer]`
"""
    return PromptTemplate(
        template=prompt,
        input_variables=["json_schema"],
    )

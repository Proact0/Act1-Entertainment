"""
노드 클래스 모듈

해당 클래스 모듈은 각각 노드 클래스가 BaseNode를 상속받아 노드 클래스를 구현하는 모듈입니다.
"""

import re

from agents.image.modules.chains import get_outfit_prompt_chain, get_storyboard_chain


def generate_storyboard_node(state):
    selected_concepts = state[
        "selected_concepts"
    ]  # 1.5단계 output으로 들어온 개수 제한된 콘셉트
    concept_str = str(selected_concepts)  # JSON string 형태로 LLM에 넘김

    chain = get_storyboard_chain()
    result = chain.run({"concepts": concept_str})

    # 백틱 후처리 (```json or ``` 제거)
    result = re.sub(r"^```json|^```|```$", "", result.strip()).strip()

    import json

    storyboard = json.loads(result)
    return {**state, "storyboard": storyboard}


# outfit 프롬프트 생성을 위한 노드들
def concept_adapter_for_outfit_node(state):
    storyboard = state.get("storyboard", {})

    main_theme = storyboard.get("main_theme", "")
    summary = storyboard.get("story_summary", "")
    colors = storyboard.get("dominant_colors", [])
    textures = storyboard.get("texture_keywords", [])
    motifs = storyboard.get("visual_motifs", [])

    # 프롬프트 입력 생성
    prompt_input = (
        f"The main theme is '{main_theme}'.\n"
        f"Summary: {summary}\n"
        f"Key visual motifs: {', '.join(motifs)}\n"
        f"Colors: {', '.join(colors)}\n"
        f"Textures: {', '.join(textures)}\n\n"
        "Based on this context, create a fashion outfit that visually reflects these concepts."
    )

    return {**state, "adapted_outfit_prompt_input": prompt_input}


def generate_outfit_prompt_node(state):
    user_request = state["adapted_outfit_prompt_input"]
    chain = get_outfit_prompt_chain()
    result = chain.run({"user_request": user_request})
    return {**state, "outfit_prompt": result}


def refine_outfit_prompt_node(state):
    prompt = state["outfit_prompt"]

    # "Image Generation Prompt:" 이후 한 문장 추출
    match = re.search(
        r"Image Generation Prompt:\s*(.+)", prompt, re.DOTALL | re.IGNORECASE
    )
    if match:
        image_prompt = match.group(1).strip()
    else:
        # fallback: 첫 문단만 사용
        image_prompt = prompt.strip().split("\n\n")[0]

    image_prompt = re.sub(r"\*\*.*?\*\*", "", image_prompt)  # bold 제거
    image_prompt = re.sub(r"[^\x00-\x7F]+", "", image_prompt)  # 이모지 제거
    image_prompt = image_prompt.strip()[:800]

    return {**state, "refined_outfit_prompt": image_prompt}


def refine_outfit_prompt_with_llm_node(state):
    """
    LLM을 활용하여 생성된 의상 프롬프트를 이미지 생성에 적합한 한 문단으로 정제하는 노드

    이 노드는 outfit_prompt 필드에 저장된 스타일링 설명을 받아,
    이미지 생성 모델이 이해하기 좋은 영어 묘사로 재구성합니다.
    """

    from langchain.chains import LLMChain
    from langchain.prompts import PromptTemplate

    from agents.image.modules.chains import get_llm

    prompt_template = PromptTemplate.from_template(
        "다음은 의상 스타일링 결과입니다.\n\n{raw_prompt}\n\n"
        "위 결과에서 '**Image Generation Prompt:**' 문단만 참고하여 아래 요구를 따르세요:\n"
        "- 하나의 문장만 생성하세요.\n"
        "- 문장 외의 설명, 인삿말, 주석은 절대 포함하지 마세요.\n"
        "- 인물과 의상을 구체적으로 묘사하세요.\n"
        "- 영어로 작성하세요.\n"
        "단 하나의 문장만 출력하세요."
    )

    chain = LLMChain(llm=get_llm(), prompt=prompt_template)
    raw_prompt = state["outfit_prompt"]
    refined_prompt = chain.run({"raw_prompt": raw_prompt})

    return {**state, "refined_outfit_prompt": refined_prompt.strip()}


# # 포즈 프롬프트 생성을 위한 노드들


def concept_adapter_for_pose_node(state):
    storyboard = state.get("storyboard", {})

    main_theme = storyboard.get("main_theme", "")
    summary = storyboard.get("story_summary", "")
    colors = storyboard.get("dominant_colors", [])
    textures = storyboard.get("texture_keywords", [])
    motifs = storyboard.get("visual_motifs", [])

    # 프롬프트 입력 생성
    prompt_input = (
        f"The main theme is '{main_theme}'.\n"
        f"Summary: {summary}\n"
        f"Key visual motifs: {', '.join(motifs)}\n"
        f"Colors: {', '.join(colors)}\n"
        f"Textures: {', '.join(textures)}\n\n"
        "Based on this context, create a description of a facial expression and pose that visually represents these emotions and objects."
    )

    return {**state, "adapted_pose_prompt_input": prompt_input}


def generate_pose_prompt_node(state):
    from agents.image.modules.chains import get_pose_prompt_chain

    user_request = state["adapted_pose_prompt_input"]
    chain = get_pose_prompt_chain()
    result = chain.run(user_request)
    return {**state, "pose_prompt": result}


def refine_pose_prompt_with_llm_node(state):
    from langchain.chains import LLMChain
    from langchain.prompts import PromptTemplate

    from agents.image.modules.chains import get_llm

    prompt_template = PromptTemplate.from_template(
        "다음은 포즈 스타일링 결과입니다.\n\n{raw_prompt}\n\n"
        "위 내용에서 포즈와 표정에 관한 부분만 참고하여 영어로 하나의 문장으로 정리하세요.\n"
        "- 문장은 명확하고 생생해야 하며, 시선 방향, 표정의 감정, 몸의 자세가 들어가야 합니다.\n"
        "- 포즈를 사진으로 또는 그림으로 표현하기 좋도록 적절하고 구체적으로 묘사하세요.\n"
        "- 문장 외의 설명, 제목 등은 포함하지 마세요.\n"
        "- 반드시 하나의 영어 문장만 출력하세요."
    )

    chain = LLMChain(llm=get_llm(), prompt=prompt_template)
    raw_prompt = state["pose_prompt"]
    refined = chain.run({"raw_prompt": raw_prompt})
    return {**state, "refined_pose_prompt": refined.strip()}


# 헤어 프롬프트 생성을 위한 노드들


def concept_adapter_for_hair_node(state):
    storyboard = state.get("storyboard", {})

    main_theme = storyboard.get("main_theme", "")
    summary = storyboard.get("story_summary", "")
    colors = storyboard.get("dominant_colors", [])
    textures = storyboard.get("texture_keywords", [])
    motifs = storyboard.get("visual_motifs", [])

    # 프롬프트 입력 생성
    prompt_input = (
        f"The main theme is '{main_theme}'.\n"
        f"Summary: {summary}\n"
        f"Key visual motifs: {', '.join(motifs)}\n"
        f"Colors: {', '.join(colors)}\n"
        f"Textures: {', '.join(textures)}\n\n"
        "🎯 Your task:\n"
        "**ONLY** describe a suitable **hairstyle** that reflects the above mood, texture, and symbols.\n"
        "Do NOT describe facial expression, body posture, outfit, or background. Focus on the hairstyle only.\n\n"
        "Include details such as:\n"
        "- hair length\n"
        "- shape and silhouette\n"
        "- texture and volume\n"
        "- movement (e.g., flowing, tied, layered)\n"
        "- color (linked to the given palette)\n\n"
        "Respond in English, and keep the style vivid but concise."
    )

    return {**state, "adapted_hair_prompt_input": prompt_input}


def generate_hair_prompt_node(state):
    from agents.image.modules.chains import get_hair_prompt_chain

    user_request = state["adapted_hair_prompt_input"]
    chain = get_hair_prompt_chain()
    result = chain.run(user_request)
    return {**state, "hair_prompt": result}

from langchain_google_genai import ChatGoogleGenerativeAI

def get_gemini_model(temperature=0.7, top_p=0.9):
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=temperature,
        top_p=top_p
    )

def get_openai_model(temperature=0.7, top_p=0.9):
    """OpenAI 모델 (기존 호환성 유지)"""
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(model="gpt-4o-mini", temperature=temperature, top_p=top_p)

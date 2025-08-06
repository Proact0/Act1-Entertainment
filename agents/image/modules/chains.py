"""LangChain 체인을 설정하는 함수 모듈

LCEL(LangChain Expression Language)을 사용하여 체인을 구성합니다.
기본적으로 modules.prompt 템플릿과 modules.models 모듈을 사용하여 LangChain 체인을 생성합니다.
"""

# from langchain.schema.runnable import RunnablePassthrough, RunnableSerializable
# from langchain_core.output_parsers import StrOutputParser

# from agents.image.modules.models import get_openai_model
# from agents.image.modules.prompts import get_image_generation_prompt

# chains.py
import os

from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from pydantic import SecretStr

from agents.image.modules.prompts import (
    outfit_prompt_template,
    pose_prompt_template,
    storyboard_prompt_template,
)

load_dotenv()  # .env 파일에서 환경변수 로딩


def get_llm():
    return ChatGroq(
        api_key=SecretStr(os.getenv("GROQ_API_KEY") or ""),
        model="llama-3.3-70b-versatile",
        temperature=0,
    )


def get_outfit_prompt_chain():
    llm = ChatGroq(
        api_key=SecretStr(os.getenv("GROQ_API_KEY") or ""),
        model="llama-3.3-70b-versatile",
        temperature=0,
    )
    return LLMChain(llm=llm, prompt=outfit_prompt_template)


def get_pose_prompt_chain():
    llm = ChatGroq(
        api_key=SecretStr(os.getenv("GROQ_API_KEY") or ""),
        model="llama-3.3-70b-versatile",
        temperature=0,
    )
    return LLMChain(llm=llm, prompt=pose_prompt_template)


def get_hair_prompt_chain():
    llm = ChatGroq(
        api_key=SecretStr(os.getenv("GROQ_API_KEY") or ""),
        model="llama-3.3-70b-versatile",
        temperature=0,
    )
    return LLMChain(llm=llm, prompt=pose_prompt_template)


def get_storyboard_chain():
    return LLMChain(llm=get_llm(), prompt=storyboard_prompt_template)

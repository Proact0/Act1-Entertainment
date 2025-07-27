"""
노드 클래스 모듈

해당 클래스 모듈은 각각 노드 클래스가 BaseNode를 상속받아 노드 클래스를 구현하는 모듈입니다.
"""

import os
import base64
from datetime import datetime
from agents.base_node import BaseNode
from agents.image.modules.chains import set_image_generation_chain, set_context_chain
from typing import Dict, Any
from langchain_core.runnables import RunnableSerializable
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

from agents.text.modules.persona import PERSONA
from agents.base_node import BaseNode
from agents.image.modules.state import ImageState
from agents.image.modules.prompts import get_image_generation_prompt, get_context_prompt

import json


load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

class ImageGenerationNode(BaseNode):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
        self.chain = set_image_generation_chain()
        self.prompt = get_image_generation_prompt()
   

    def execute(self, state: ImageState) -> dict:
        prompt_chain = self.chain
        
        response = prompt_chain.invoke(
            {
                "content_topic": state['content_topic'], 
                "content_type": state['content_type'],
                "context_describe":state['context_describe'],
                "persona": state['persona']  # 페르소나 세부 정보
            }
        , generation_config = dict(response_modalities = ["TEXT"]))
        
        
        
        return {"response": response}

    
class getStoryBoardNode(BaseNode):
    """
    다른 노드로부터 온 input을 받아서, 해석하는 노드 
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
        self.chain = set_context_chain()
        self.prompt = get_context_prompt()
    
    def execute(self, state: ImageState) -> dict:
        prompt_chain = self.chain

        response = prompt_chain.invoke(
            {
                "content_topic": state['content_topic'], 
                "content_type": state['content_type'],
                "context": state['context'] , 
                "genre" : state['genre'],
                "persona": PERSONA  
            }
        , generation_config = dict(response_modalities = ["TEXT"]))

        
        return {'response':response
                }




import os
from langchain_google_genai import ChatGoogleGenerativeAI
from src.app.config import GEMINI_API_KEY

_MODEL_RAPIDO = os.getenv("GEMINI_MODEL_RAPIDO", os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite"))
_MODEL_ESPECIALISTA = os.getenv("GEMINI_MODEL_ESPECIALISTA", os.getenv("GEMINI_MODEL", "gemini-3.5-flash"))

# Modelo rápido para guardrails, roteador e orquestrador
llm_rapido = ChatGoogleGenerativeAI(
    model=_MODEL_RAPIDO,
    google_api_key=GEMINI_API_KEY,
    temperature=0.1,
    max_retries=2,
)

# Modelo especialista para análise de dados e planejamento
llm_especialista = ChatGoogleGenerativeAI(
    model=_MODEL_ESPECIALISTA,
    google_api_key=GEMINI_API_KEY,
    temperature=0.2,
    max_retries=2,
)

llm_gemini = llm_especialista
llm_groq = llm_rapido
llm = llm_rapido

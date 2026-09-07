from langchain_ollama import ChatOllama
from app.config.core import settings

def create_llm()-> ChatOllama:
    """
    Create a ChatOllama instance with the specified model and temperature."""

    return ChatOllama(
        model=settings.model
    )
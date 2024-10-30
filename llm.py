# https://medium.com/@batuhansenerr/ai-powered-financial-analysis-multi-agent-systems-transform-data-into-insights-d94e4867d75d
# https://github.com/YBSener/financial_Agent/tree/main


import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
# from langchain_groq import ChatGroq
from typing import Literal

MODEL_CLASS = Literal[
    'gpt-3.5-turbo',
    "gpt-4o",
    "gpt-4o-mini",
    "llama-3-8b-8192",
    "llama-3.1-70b-versatile",
    'llama-3.1-8b-versatile',
    "mixtral-8x7b-32768"
]

load_dotenv()
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")
os.environ["REDDIT_CLIENT_ID"] = os.getenv("REDDIT_CLIENT_ID")
os.environ["REDDIT_CLIENT_SECRET"] = os.getenv("REDDIT_CLIENT_SECRET")
os.environ["REDDIT_USER_AGENT"] = os.getenv("REDDIT_USER_AGENT")


def initialize_llm(model_option: MODEL_CLASS):

    match model_option:
        case gpt_model if "gpt" in model_option:
            return ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), model=gpt_model, temperature=0.1)
        case llama_model if "llama" in model_option:
            return ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model=llama_model, temperature=0.1)
        case mixtral_model if "mixtral" in model_option:
            return ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model=mixtral_model, temperature=0.1)
        case _:
            raise ValueError("Unknown")


if __name__ == "__main__":
    print(os.getenv("OPENAI_API_KEY"))
    llm = initialize_llm("mixtral-8x7b-32768")
    response = llm.invoke("hello")
    print(response.content)
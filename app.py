import os
import streamlit as st
from dotenv import load_dotenv

# LangChain 最新仕様
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# --- 環境変数の読み込み ---
load_dotenv()  # プロジェクト直下の .env を読み込む
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# --- LLM 初期化 ---
llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0,
    openai_api_key=OPENAI_API_KEY
)

# --- LLM問い合わせ関数 ---
def get_llm_response(user_text: str, role: str) -> str:
    """入力テキストと役割を基にLLMへ問い合わせ、回答を返す"""
    if role.startswith("A"):
        system_prompt = "あなたは経験豊富な医者です。"
    elif role.startswith("B"):
        system_prompt = "あなたは優秀な投資アドバイザーです。"

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_text),
    ]

    result = llm(messages)
    return result.content

# --- Streamlit UI ---
st.title("💬 LangChain + Streamlit Demo")

role = st.radio(
    "専門家の種類を選んでください:",
    ("A: 医者", "B: 投資アドバイザー")
)

user_input = st.text_area("質問を入力してください:")

if st.button("送信"):
    if user_input.strip() == "":
        st.warning("質問を入力してください。")
    else:
        with st.spinner("回答を生成中..."):
            response = get_llm_response(user_input, role)
        st.subheader("回答:")
        st.write(response)
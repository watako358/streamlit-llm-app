from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# OpenAI APIを利用するLLMを初期化
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

# --- LLM問い合わせ関数 ---
def get_llm_response(user_text: str, role: str) -> str:
    """入力テキストと役割を基にLLMへ問い合わせ、回答を返す"""
    if role.startswith("C"):
        system_prompt = "あなたは経験豊富な医者です。"
    elif role.startswith("D"):
        system_prompt = "あなたは優秀な投資アドバイザーです。"
    else:
        system_prompt = "あなたは博識な専門家です。"

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_text),
    ]

    result = llm(messages)
    return result.content

# --- Streamlit UI ---
st.title("💬 LangChain + Streamlit Demo")

# ラジオボタンで専門家の種類を選択
role = st.radio(
    "専門家の種類を選んでください:",
    ("C: 医者", "D: 投資アドバイザー")
)

# 入力フォーム
user_input = st.text_area("質問を入力してください:")

# 送信ボタン
if st.button("送信"):
    if user_input.strip() == "":
        st.warning("質問を入力してください。")
    else:
        with st.spinner("回答を生成中..."):
            response = get_llm_response(user_input, role)
        st.subheader("回答:")
        st.write(response)
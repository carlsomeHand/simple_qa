import os
import streamlit as st
from openai import OpenAI
from streamlit.logger import get_logger

from config import CORPUS

LOGGER = get_logger(__name__)

with open(CORPUS, 'r', encoding='utf-8') as f:
    corpus = f.read()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def run():
    def text_generator():
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-3.5-turbo",
            stream=True,
        )

        full_answer = ""

        for chunk in chat_completion:
            if hasattr(chunk.choices[0].delta, "content"):
                character = chunk.choices[0].delta.content
                if type(character) is str and len(character) > 0:
                    full_answer = "".join([full_answer, character])
                    yield character

        LOGGER.info(f'answer: {full_answer}')

    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.title("Welcome to the Chatbot👋")

    # 文本输入
    query = st.text_input('You can ask anything about Sam Altman(according to Wikipedia) by Chatgpt',
                          'Who is Sam Altman?')

    prompt = f"According to the text from Wikipedia, please answer the question below.\n\n" \
             f"Q: {query}\n\n" \
             f"Wikipedia text: {corpus}"

    # 通过点击按钮，调用生成器形成流式输出
    flag = st.button("Get answer", type="primary")
    if flag:
        LOGGER.info(f'user query: {query}')
        st.write_stream(text_generator)
        st.write("\n Is this conversation helpful so far?")
        if st.button("Good"):
            LOGGER.info('user feedback: Good')
            st.rerun()
        if st.button("Bad"):
            LOGGER.info('user feedback: Bad')


if __name__ == "__main__":
    run()


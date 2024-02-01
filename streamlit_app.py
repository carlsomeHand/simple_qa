import openai
import streamlit as st
from streamlit.logger import get_logger

from config import CORPUS, api_key


LOGGER = get_logger(__name__)

with open(CORPUS, 'r', encoding='utf-8') as f:
    corpus = f.read()

LOGGER.info(f'corpus: {CORPUS}')

def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    client = OpenAI(api_key=api_key)
    
    query = st.text_input('You can ask anything about Sam Altman(according to Wikipedia)', 'Hello.')


    prompt = f"According to the text from Wikipedia, please answer the question below.\n\n" \
             f"Q: {query}\n\n" \
             f"Wikipedia text: {corpus}"

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )

    answer_text = ""

    for chunk in completion:
        if hasattr(chunk.choices[0].delta, "content"):
            answer_text = "".join([answer_text, chunk.choices[0].delta.content])
            st.write(answer_text)


if __name__ == "__main__":
    run()
    
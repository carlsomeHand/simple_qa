import os
import streamlit as st
from openai import OpenAI
from streamlit.logger import get_logger

from config import CORPUS

LOGGER = get_logger(__name__)

with open(CORPUS, 'r', encoding='utf-8') as f:
    corpus = f.read()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# LOGGER.info(f'corpus: {CORPUS}')


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

        for chunk in chat_completion:
            if hasattr(chunk.choices[0].delta, "content"):
                if type(chunk.choices[0].delta.content) is str:
                    yield chunk.choices[0].delta.content

    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )
    # LOGGER.info(f"api_key:{api_key}")

    query = st.text_input('You can ask anything about Sam Altman(according to Wikipedia)', 'Who is Sam Altman?')

    prompt = f"According to the text from Wikipedia, please answer the question below.\n\n" \
             f"Q: {query}\n\n" \
             f"Wikipedia text: {corpus}"

    if st.button("Answer"):
        st.write_stream(text_generator)


if __name__ == "__main__":
    run()


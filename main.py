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

    try:
        openai.api_key = api_key
    except ImportError:
        raise ValueError(
            "Could not import openai python package. "
            "Please install it with `pip install openai`."
        )

    query = st.text_input('You can ask anything about Sam Altman(according to Wikipedia)', '')

    prompt = f"According to the text from Wikipedia, please answer the question below.\n\n" \
             f"Q: {query}\n\n" \
             f"Wikipedia text: {corpus}"

    completion = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.7,
        stream=True
    )

    """
    completion = openai.ChatCompletion.create(
        model="text-davinci-002",
        messages=messages,
        stream=True
    )
    """

    answer_text = ""

    for chunk in completion:
        if hasattr(chunk.choices[0].delta, "content"):
            answer_text = "".join([answer_text, chunk.choices[0].delta.content])
            st.write(answer_text)


if __name__ == "__main__":
    run()
    

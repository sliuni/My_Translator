import streamlit as st
from deep_translator import GoogleTranslator

st.title("Interactive Word Translator 🖱️")
st.subheader("Нажми на слово, чтобы узнать перевод")

# 1. Поле для ввода большого куска текста
input_text = st.text_area("Вставь текст на английском сюда:", "Learning Python is fun and easy")

if input_text:
    # 2. Разделяем текст на слова
    words = input_text.split()
    
    st.write("---")
    st.write("### Твой текст (нажимай на слова):")
    
    # Создаем контейнер, чтобы кнопки шли друг за другом, а не в столбик
    cols = st.container()
    
    # 3. Создаем кнопки для каждого слова
    # Мы используем уникальный ключ для каждой кнопки, чтобы Streamlit не путался
    for index, word in enumerate(words):
        if st.button(word, key=f"word_{index}"):
            # 4. Перевод конкретного слова при нажатии
            translation = GoogleTranslator(source='auto', target='ru').translate(word)
            st.info(f"**{word}** — это: **{translation}**")

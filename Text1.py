import streamlit as st
from deep_translator import GoogleTranslator

# Настройка стилей, чтобы кнопки выглядели как обычный текст
st.markdown("""
    <style>
    div.stButton > button {
        border: none;
        padding: 0px 2px;
        background-color: transparent;
        color: inherit;
        font-size: 18px;
        vertical-align: baseline;
    }
    div.stButton > button:hover {
        color: #ff4b4b;
        background-color: transparent;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Smart Reading 📖")

input_text = st.text_area("Вставь текст здесь:", "Python is an interpreted high-level general-purpose programming language.")

if input_text:
    words = input_text.split()
    
    st.write("---")
    
    # Создаем область, где слова будут выстраиваться в строку
    # Используем unsafe_allow_html для гибкой верстки
    t_container = st.container()
    
    # Выводим слова в одну строку (флекс-контейнер)
    html_string = "<div style='display: flex; flex-wrap: wrap; gap: 5px; line-height: 2;'>"
    
    # В Streamlit кнопки всегда создают новый элемент, 
    # поэтому мы используем колонки или специальную верстку
    cols = st.columns(len(words) if len(words) > 0 else 1)
    
    for i, word in enumerate(words):
        with cols[i % len(cols)]: # Это заставит их идти в ряд
            if st.button(word, key=f"btn_{i}"):
                clean_word = word.strip(".,!?;:()")
                translation = GoogleTranslator(source='auto', target='ru').translate(clean_word)
                st.sidebar.success(f"**{clean_word}** = {translation}")

st.sidebar.info("Нажми на слово в тексте, чтобы увидеть перевод здесь.")

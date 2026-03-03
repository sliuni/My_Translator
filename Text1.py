import streamlit as st
from deep_translator import GoogleTranslator
# 1. Получаем список всех доступных языков автоматически
translator_instance = GoogleTranslator()
langs_dict = translator_instance.get_supported_languages(as_dict=True)

# 2. Делаем названия языков с большой буквы для красоты в меню
langs = {k.capitalize(): v for k, v in langs_dict.items()}

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
# Создаем выпадающий список в боковой панели
choice = st.sidebar.selectbox("Выберите язык:", list(langs.keys()))

input_text = st.text_area("Вставь текст здесь:", "High-level translater of language by general-purpose.")

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
                translation = GoogleTranslator(source='auto', target=langs[choice]).translate(clean_word)
                st.sidebar.success(f"**{clean_word}** = {translation}")

st.sidebar.info("Нажми на слово в тексте, чтобы увидеть перевод здесь.")




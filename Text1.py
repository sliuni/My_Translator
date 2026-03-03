import streamlit as st
from deep_translator import GoogleTranslator

# 1. Получаем список всех доступных языков автоматически
translator_instance = GoogleTranslator()
langs_dict = translator_instance.get_supported_languages(as_dict=True)
# Делаем первую букву заглавной для меню
langs = {k.capitalize(): v for k, v in langs_dict.items()}

# 2. Настройка стилей (CSS)
st.markdown("""
    <style>
    /* Уплотняем кнопки в одну строку */
    div.stButton {
        display: inline-block !important;
        margin-right: -8px !important;
    }
    /* Делаем их похожими на текст */
    div.stButton > button {
        border: none;
        padding: 0px 4px !important;
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

# 3. Боковая панель
st.sidebar.title("Настройки")
choice = st.sidebar.selectbox("Выберите язык перевода:", list(langs.keys()))

# 4. Основное окно
input_text = st.text_area("Вставь текст здесь:", "High-level translator of language by general-purpose.")

    # Просто запускаем цикл — кнопки сами выстроятся в ряд благодаря CSS выше
      if input_text:
         words = input_text.split()  # ТУТ ОТСТУП
         st.write("---")             # ТУТ ОТСТУП
    
    # 5. Самый важный цикл: выводим слова БЕЗ колонок
    for i, word in enumerate(words):
        if st.button(word, key=f"btn_{i}"):
            clean_word = word.strip(".,!?;:()")
            # Переводим на выбранный язык
            translation = GoogleTranslator(source='auto', target=langs[choice]).translate(clean_word)
            st.sidebar.success(f"**{clean_word}** = {translation}")

st.sidebar.info("Нажми на слово в тексте, чтобы увидеть перевод выше.")









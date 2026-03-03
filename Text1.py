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
    /* 1. Заставляем каждую колонку сжиматься под размер слова */
    [data-testid="column"] {
        width: auto !important;
        flex: none !important;
        padding-left: 0px !important;
        padding-right: 2px !important; /* Узкий пробел между словами */
    }

    /* 2. Убираем стандартные отступы самого контейнера колонок */
    [data-testid="stHorizontalBlock"] {
        gap: 0px !important;
        justify-content: flex-start !important;
    }

    /* 3. Делаем кнопки невидимыми (как обычный текст) */
    div.stButton > button {
        border: none;
        padding: 0px 2px !important;
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

if input_text:
    words = input_text.split()
    st.write("---")
    
    # ТОТ САМЫЙ ПЕРВЫЙ ВАРИАНТ:
    # Создаем сетку колонок по количеству слов
    cols = st.columns(len(words) if len(words) > 0 else 1)
    
    for i, word in enumerate(words):
        with cols[i]:
            if st.button(word, key=f"btn_{i}"):
                clean_word = word.strip(".,!?;:()")
                # Перевод на выбранный язык
                translation = GoogleTranslator(source='auto', target=langs[choice]).translate(clean_word)
                st.sidebar.success(f"**{clean_word}** = {translation}")

st.sidebar.info("Нажми на слово в тексте, чтобы увидеть перевод выше.")


















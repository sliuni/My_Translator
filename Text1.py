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
    /* ПРИНУДИТЕЛЬНО делаем контейнеры кнопок маленькими */
    div.stButton {
        display: inline-block !important;
        width: auto !important;
        margin-right: -4px !important; /* Еще плотнее */
    }
    
    /* Убираем стандартные отступы Streamlit для кнопок */
    div.stButton > button {
        border: none;
        padding: 0px 2px !important;
        background-color: transparent;
        color: inherit;
        font-size: 18px;
        vertical-align: baseline;
        width: auto !important; /* Чтобы кнопка не была на всю строку */
    }

    div.stButton > button:hover {
        color: #ff4b4b;
    }
    
    /* Убираем лишние отступы между колонками, если они остались */
    [data-testid="column"] {
        width: auto !important;
        flex: none !important;
    }
    [data-testid="stHorizontalBlock"] {
        gap: 0px !important;
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
    
    # План «Монолит»: Оборачиваем все кнопки в один flex-контейнер
    # Это заставит их идти друг за другом и переноситься как обычный текст
    st.markdown('<div style="display: flex; flex-wrap: wrap; gap: 0px; align-items: baseline;">', unsafe_allow_html=True)
    
    # Создаем область, где кнопки будут выводиться в ряд
    container = st.container()
    with container:
        # Важно: просто выводим кнопки одну за другой БЕЗ колонок
        for i, word in enumerate(words):
            if st.button(word, key=f"word_{i}"):
                clean_word = word.strip(".,!?;:()")
                translation = GoogleTranslator(source='auto', target=langs[choice]).translate(clean_word)
                st.sidebar.success(f"**{clean_word}** = {translation}")
    
    st.markdown('</div>', unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)

# Эта строка стоит у края, она вне условия if
st.sidebar.info("Нажми на слово в тексте, чтобы увидеть перевод выше.")















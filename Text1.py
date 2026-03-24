import streamlit as st

# Настройка страницы (делаем ее широкой)
st.set_page_config(layout="wide")

st.title("Smart Reading Assistant 📖")

# Создаем две колонки: 
# col1 (левая) — 70% ширины для текста и перевода
# col2 (правая) — 30% ширины для советов ИИ
col1, col2 = st.columns([7, 3])

with col1:
    st.header("Твой текст")
    user_input = st.text_area("Введите предложение для разбора:", placeholder="Например: Learning Python is fun!")
    
    # Твоя прошлая логика перевода (пример)
    if user_input:
        st.info(f"Здесь будет твой перевод по словам...")
        # Тут мы вставим твой цикл со словами, который мы обсуждали раньше
        words = user_input.split()
        cols = st.columns(len(words))
        for i, word in enumerate(words):
            with cols[i]:
                st.button(word, key=f"btn_{i}")

with col2:
    st.header("ChatGPT AI ✨")
    st.write("---") # Разделительная линия
    
    # Контейнер для ответа от нейросети
    if user_input:
        with st.spinner('ИИ анализирует текст...'):
            # Пока у нас нет ключа API, сделаем "заглушку"
            st.success(f"**Анализ фразы:** '{user_input}'")
            st.write("💡 **Совет от ИИ:** В этом предложении используется Present Continuous. Глагол 'learning' выступает в роли подлежащего.")
            st.caption("Когда мы подключим OpenAI API, здесь будет реальный ответ.")
    else:
        st.write("Введите текст слева, чтобы получить подсказку от ИИ.")

# Добавляем немного CSS, чтобы колонки не "разлетались" на мобильных
st.markdown("""
    <style>
    [data-testid="column"] {
        padding: 10px;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

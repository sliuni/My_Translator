import streamlit as st

# Инициализируем память для выбранного слова, если её ещё нет
if "selected_word" not in st.session_state:
    st.session_state.selected_word = None

# ... (остальной код сверху остается таким же) ...

with col1:
    st.header("Твой текст")
    user_input = st.text_area("Введите предложение:", placeholder="Например: Learning Python is fun!")
    
    if user_input:
        st.write("---")
        words = user_input.split()
        
        # Создаем сетку из кнопок
        cols = st.columns(len(words))
        for i, word in enumerate(words):
            # Чистим слово от знаков препинания для красоты
            clean_word = word.strip(".,!?;:")
            
            # Если кнопка нажата, записываем слово в память
            if cols[i].button(clean_word, key=f"btn_{i}"):
                st.session_state.selected_word = clean_word

        # Если в памяти есть выбранное слово — показываем его
        if st.session_state.selected_word:
            st.markdown(f"### Выбрано слово: **{st.session_state.selected_word}**")
            # Сюда мы позже добавим автоматический перевод этого конкретного слова
            st.info(f"Тут будет перевод для слова '{st.session_state.selected_word}'")

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

import streamlit as st

# 1. Настройка страницы (должна быть самой первой командой Streamlit)
st.set_page_config(layout="wide", page_title="Smart Reading AI")

# 2. Инициализация "памяти" приложения (Session State)
# Это нужно, чтобы приложение помнило, какое слово мы нажали
if "selected_word" not in st.session_state:
    st.session_state.selected_word = None

st.title("Smart Reading Assistant 📖")

# 3. Создание колонок: левая (70%) и правая (30%)
col1, col2 = st.columns([7, 3])

# --- ЛЕВАЯ КОЛОНКА ---
with col1:
    st.header("Твой текст")
    user_input = st.text_area("Введите предложение для разбора:", 
                              placeholder="Например: I am learning Python step by step",
                              height=150)
    
    if user_input:
        st.write("### Нажми на слово для анализа:")
        words = user_input.split()
        
        # Рисуем кнопки для каждого слова
        # Используем контейнер, чтобы кнопки шли в ряд, если их много
        word_buttons_container = st.container()
        word_cols = st.columns(len(words) if len(words) > 0 else 1)
        
        for i, word in enumerate(words):
            clean_word = word.strip(".,!?;:()\"")
            # Если кнопка нажата, записываем слово в "память"
            if word_cols[i].button(clean_word, key=f"btn_{i}"):
                st.session_state.selected_word = clean_word

# --- ПРАВАЯ КОЛОНКА ---
with col2:
    st.header("ChatGPT AI ✨")
    st.write("---")
    
    if st.session_state.selected_word:
        st.subheader(f"Анализ слова: `{st.session_state.selected_word}`")
        
        with st.spinner('ИИ готовит объяснение...'):
            # Это блок-заглушка. Когда подключим API, здесь будет реальный ответ
            st.info(f"Здесь появится подробный разбор слова **{st.session_state.selected_word}**.")
            st.write(f"**Контекст:** Ты выбрал это слово из своего текста.")
            st.write("---")
            st.write("🤖 *ИИ подсказка:* Чтобы получить реальный ответ от GPT, нам нужно вставить твой API Key в код.")
            
        # Кнопка для сброса выбора
        if st.button("Очистить выбор"):
            st.session_state.selected_word = None
            st.rerun()
    else:
        st.info("Выбери слово слева, чтобы ИИ объяснил его значение или грамматику.")

# 4. Немного красоты (CSS)
st.markdown("""
    <style>
    div[data-testid="column"] {
        padding: 20px;
        border: 1px solid #e6e9ef;
        border-radius: 15px;
        background-color: #ffffff;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        border: 1px solid #ff4b4b;
        color: #ff4b4b;
    }
    .stButton>button:hover {
        background-color: #ff4b4b;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

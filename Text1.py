import streamlit as st

# 1. Настройка страницы
st.set_page_config(layout="wide", page_title="Smart Reading AI")

# --- ТВОЙ КЛЮЧ API ---
# Вставь свой ключ между кавычками ниже
MY_OPENAI_KEY = "ЗДЕСЬ_ТВОЙ_КЛЮЧ_API" 

# Инициализация клиента OpenAI

# 2. Память приложения
if "selected_word" not in st.session_state:
    st.session_state.selected_word = None

st.title("Smart Reading Assistant 📖")

# 3. Создание колонок
col1, col2 = st.columns([6, 4])

# --- ЛЕВАЯ КОЛОНКА ---
with col1:
    st.header("Твой текст")
    user_input = st.text_area("Введите текст для разбора:", 
                              placeholder="Например: Ich lerne Python Schritt für Schritt",
                              height=150)
    
    if user_input:
        st.write("### Нажми на слово:")
        
        # Чтобы не было "водопада", используем flex-контейнер через HTML
        # Но для простоты в Streamlit сделаем вывод слов кнопками в один ряд
        words = user_input.split()
        
        # Создаем контейнер для кнопок, чтобы они не растягивались на весь экран
        cols = st.columns(10) # Фиксируем 10 колонок, чтобы они были компактными
        for i, word in enumerate(words):
            clean_word = word.strip(".,!?;:()\"")
            with cols[i % 10]: # Распределяем слова по 10 в ряд
                if st.button(clean_word, key=f"btn_{i}"):
                    st.session_state.selected_word = clean_word

# --- ПРАВАЯ КОЛОНКА ---
with col2:
    st.header("ChatGPT AI ✨")
    st.write("---")
    
    if st.session_state.selected_word:
        st.subheader(f"Разбор слова: `{st.session_state.selected_word}`")
        
        with st.spinner('Спрашиваю у нейросети...'):
            try:
                # ЗАПРОС К CHATGPT
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo", # Или gpt-4o если есть доступ
                    messages=[
                        {"role": "system", "content": "Ты учитель иностранных языков. Кратко переведи слово и объясни его грамматическую роль в предложении."},
                        {"role": "user", "content": f"Объясни слово '{st.session_state.selected_word}' из текста: {user_input}"}
                    ],
                    max_tokens=150
                )
                
                # Выводим реальный ответ
                answer = response.choices[0].message.content
                st.write(answer)
                
            except Exception as e:
                st.error("Ошибка подключения к ИИ!")
                st.info("Проверь свой API Key или баланс на аккаунте OpenAI.")
                st.caption(f"Техническая инфо: {e}")
        
        if st.button("Очистить выбор"):
            st.session_state.selected_word = None
            st.rerun()
    else:
        st.info("Нажми на слово слева, чтобы ИИ проанализировал его.")

# 4. Стили (исправляем "водопад" и внешний вид)
st.markdown("""
    <style>
    div[data-testid="column"] {
        padding: 15px;
        border-radius: 10px;
    }
    .stButton>button {
        padding: 2px 5px;
        font-size: 14px;
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

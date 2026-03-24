import streamlit as st
import google.generativeai as genai

# 1. Настройка страницы
st.set_page_config(layout="wide", page_title="Smart Reading AI")

# Проверка ключа в Secrets
if "GEMINI_API_KEY" not in st.secrets:
    st.error("⚠️ Ключ не найден в Secrets! Добавь GEMINI_API_KEY в настройках Streamlit Cloud.")
    st.stop()

# Настройка Gemini с исправлением ошибки 404
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Используем проверенное название модели
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
except Exception as e:
    st.error(f"Ошибка настройки: {e}")

# Память для выбранного слова
if "selected_word" not in st.session_state:
    st.session_state.selected_word = None

st.title("Smart Reading Assistant 📖")

# 2. Колонки
col_left, col_right = st.columns([4, 6]) # Сделали левую колонку чуть уже

with col_left:
    st.header("Твой текст")
    user_text = st.text_area("Вставь текст для разбора:", 
                              placeholder="Ich lerne Python...",
                              height=150)
    
    if user_text:
        st.write("### Нажми на слово:")
        words = user_text.split()
        
        # ВОЗВРАЩАЕМ ВЕРТИКАЛЬНЫЕ СТОЛБИКИ
        # Теперь каждое слово — это кнопка на новой строке
        for i, word in enumerate(words):
            clean_word = word.strip(".,!?;:()\"")
            # Кнопка на всю ширину колонки
            if st.button(clean_word, key=f"btn_{i}"):
                st.session_state.selected_word = clean_word

with col_right:
    st.header("Gemini AI ✨")
    st.write("---")
    
    if st.session_state.selected_word:
        st.subheader(f"Разбор слова: `{st.session_state.selected_word}`")
        
        with st.spinner('Gemini анализирует...'):
            try:
                prompt = f"""
                Ты профессиональный учитель. 
                1. Переведи слово '{st.session_state.selected_word}' на русский.
                2. Объясни его грамматику в предложении: '{user_text}'.
                3. Дай один короткий пример использования.
                Пиши очень кратко.
                """
                # Добавляем параметр для стабильности
                response = model.generate_content(prompt)
                
                if response.text:
                    st.write(response.text)
                else:
                    st.warning("ИИ не смог сгенерировать текст. Попробуй другое слово.")
                    
            except Exception as e:
                st.error("Ошибка при связи с ИИ.")
                st.caption(f"Техническая деталь: {e}")
        
        if st.button("Очистить выбор"):
            st.session_state.selected_word = None
            st.rerun()
    else:
        st.info("Выбери слово в столбике слева.")

# 3. Стили для удобных столбиков
st.markdown("""
    <style>
    /* Делаем кнопки в столбик узкими и аккуратными */
    .stButton>button {
        width: 100%;
        border-radius: 4px;
        padding: 5px;
        margin-bottom: 2px;
        background-color: white;
        text-align: left; /* Текст слова слева, как в списке */
        border: 1px solid #ddd;
    }
    .stButton>button:hover {
        background-color: #f0f2f6;
        border-color: #ff4b4b;
    }
    /* Делаем колонку со словами прокручиваемой, если слов очень много */
    [data-testid="column"]:nth-child(1) {
        max-height: 80vh;
        overflow-y: auto;
    }
    </style>
    """, unsafe_allow_html=True)

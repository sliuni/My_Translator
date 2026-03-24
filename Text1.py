import streamlit as st
import google.generativeai as genai

# 1. Настройка страницы
st.set_page_config(layout="wide", page_title="Smart Reading AI")

# Проверка наличия ключа в Secrets
if "GEMINI_API_KEY" not in st.secrets:
    st.error("⚠️ Ключ не найден в Secrets! Проверь настройки на share.streamlit.io")
    st.stop()

# Настройка Gemini
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Ошибка настройки ИИ: {e}")

# Память для выбранного слова
if "selected_word" not in st.session_state:
    st.session_state.selected_word = None

st.title("Smart Reading Assistant 📖")

# 2. Колонки
col_left, col_right = st.columns([6, 4])

with col_left:
    st.header("Твой текст")
    user_text = st.text_area("Вставь текст для разбора:", 
                              placeholder="Например: Ich lerne Python...",
                              height=200)
    
    if user_text:
        st.write("### Нажми на слово:")
        # Используем split() без параметров, чтобы он убирал лишние пробелы и переносы
        words = user_text.split()
        
        # Группируем кнопки по 5-6 штук в ряд
        row_size = 6
        for i in range(0, len(words), row_size):
            cols = st.columns(row_size)
            row_words = words[i:i + row_size]
            for j, word in enumerate(row_words):
                clean_word = word.strip(".,!?;:()\"")
                if cols[j].button(clean_word, key=f"btn_{i+j}"):
                    st.session_state.selected_word = clean_word

with col_right:
    st.header("Gemini AI ✨")
    st.write("---")
    
    if st.session_state.selected_word:
        st.subheader(f"Слово: `{st.session_state.selected_word}`")
        
        with st.spinner('Gemini анализирует...'):
            try:
                # Четкий промпт для лучшего результата
                prompt = f"""
                Ты профессиональный учитель иностранных языков. 
                1. Переведи слово '{st.session_state.selected_word}' на русский.
                2. Объясни грамматику этого слова в контексте предложения: '{user_text}'.
                3. Дай один короткий пример использования.
                Пиши кратко и только по делу.
                """
                response = model.generate_content(prompt)
                
                if response.text:
                    st.write(response.text)
                else:
                    st.warning("ИИ вернул пустой ответ. Попробуй другое слово.")
                    
            except Exception as e:
                st.error("Ошибка при связи с ИИ.")
                st.caption(f"Техническая деталь: {e}")
        
        if st.button("Очистить выбор"):
            st.session_state.selected_word = None
            st.rerun()
    else:
        st.info("Нажми на слово слева, чтобы получить разбор.")

# 3. Красивые стили
st.markdown("""
    <style>
    /* Делаем кнопки одинаковыми и красивыми */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background-color: #ffffff;
        border: 1px solid #d1d5db;
        color: #374151;
        font-weight: 500;
    }
    .stButton>button:hover {
        border-color: #ff4b4b;
        color: #ff4b4b;
        background-color: #fff5f5;
    }
    /* Рамки для колонок */
    div[data-testid="column"] {
        padding: 20px;
        border-radius: 15px;
        background-color: #f9fafb;
        border: 1px solid #f3f4f6;
    }
    </style>
    """, unsafe_allow_html=True)

import streamlit as st
import google.generativeai as genai

# 1. Настройка страницы
st.set_page_config(layout="wide", page_title="Smart Reading Assistant")

# Проверка ключа в Secrets
if "GEMINI_API_KEY" not in st.secrets:
    st.error("⚠️ Ключ не найден в Secrets! Сначала исправь ошибку в настройках Streamlit.")
    st.stop()

# Настройка Gemini
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Инициализация памяти приложения
if "selected_word" not in st.session_state:
    st.session_state.selected_word = None

st.title("Smart Reading Assistant 📖")

# 3. Создание колонок: Левая для текста, Правая для ИИ
col_text, col_ai = st.columns([6, 4])

with col_text:
    st.header("Твой текст")
    user_input = st.text_area("Вставь текст (например, на немецком):", 
                              placeholder="Ich wohne в Ludwigshafen...",
                              height=200)
    
    if user_input:
        st.write("### Нажми на слово для разбора:")
        words = user_input.split()
        
        # Группируем кнопки, чтобы они не падали в "водопад"
        # Создаем контейнер для кнопок
        container = st.container()
        row_size = 7 # Количество слов в одной строке
        for i in range(0, len(words), row_size):
            cols = st.columns(row_size)
            row_words = words[i:i + row_size]
            for j, word in enumerate(row_words):
                clean_word = word.strip(".,!?;:()\"")
                if cols[j].button(clean_word, key=f"btn_{i+j}"):
                    st.session_state.selected_word = clean_word

with col_ai:
    st.header("Gemini AI ✨")
    st.write("---")
    
    if st.session_state.selected_word:
        st.subheader(f"Слово: `{st.session_state.selected_word}`")
        
        with st.spinner('Gemini анализирует...'):
            try:
                # Промпт для учителя
                prompt = f"""
                Ты профессиональный лингвист и учитель. 
                Дай перевод слова '{st.session_state.selected_word}' на русский.
                Объясни его грамматическую форму в этом контексте: '{user_input}'.
                Пиши кратко, 3-4 предложения.
                """
                response = model.generate_content(prompt)
                st.write(response.text)
            except Exception as e:
                st.error(f"Произошла ошибка: {e}")
        
        if st.button("Очистить"):
            st.session_state.selected_word = None
            st.rerun()
    else:
        st.info("Выбери слово слева, чтобы получить объяснение от ИИ.")

# Стили для аккуратного вида
st.markdown("""
    <style>
    .stButton>button { width: 100%; font-size: 14px; margin-bottom: 5px; }
    div[data-testid="column"] { border: 1px solid #f0f2f6; padding: 15px; border-radius: 12px; background-color: #fdfdfd; }
    </style>
    """, unsafe_allow_html=True)

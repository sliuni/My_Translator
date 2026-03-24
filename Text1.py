import streamlit as st
import google.generativeai as genai

# 1. Настройка страницы
st.set_page_config(layout="wide", page_title="Smart Reading AI (Gemini)")

# БЕЗОПАСНОЕ ПОДКЛЮЧЕНИЕ КЛЮЧА GEMINI
# В настройках Streamlit Secrets назови ключ GEMINI_API_KEY
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Ошибка: Ключ GEMINI_API_KEY не найден в Secrets!")
    st.stop()

# Настройка Gemini
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Память приложения
if "selected_word" not in st.session_state:
    st.session_state.selected_word = None

st.title("Smart Reading Assistant (Gemini Edition) 📖")

# 3. Создание колонок
col1, col2 = st.columns([6, 4])

with col1:
    st.header("Твой текст")
    user_input = st.text_area("Введите текст для разбора:", 
                              placeholder="Например: Ich lerne Python Schritt für Schritt",
                              height=150)
    
    if user_input:
        st.write("### Нажми на слово:")
        words = user_input.split()
        
        # Группируем кнопки по 8 штук в ряд
        row_size = 8
        for i in range(0, len(words), row_size):
            row_words = words[i:i + row_size]
            cols = st.columns(row_size)
            for j, word in enumerate(row_words):
                clean_word = word.strip(".,!?;:()\"")
                if cols[j].button(clean_word, key=f"btn_{i+j}"):
                    st.session_state.selected_word = clean_word

with col2:
    st.header("Gemini AI ✨")
    st.write("---")
    
    if st.session_state.selected_word:
        st.subheader(f"Разбор слова: `{st.session_state.selected_word}`")
        
        with st.spinner('Gemini думает...'):
            try:
                # ЗАПРОС К GEMINI
                prompt = f"""
                Ты учитель иностранных языков. 
                Кратко переведи слово '{st.session_state.selected_word}' на русский язык 
                и объясни его грамматическую роль в предложении: '{user_input}'.
                Пиши кратко и понятно.
                """
                response = model.generate_content(prompt)
                
                st.write(response.text)
                
            except Exception as e:
                st.error("Ошибка API Gemini.")
                st.caption(f"Подробности: {e}")
        
        if st.button("Очистить выбор"):
            st.session_state.selected_word = None
            st.rerun()
    else:
        st.info("Нажми на слово слева, чтобы Gemini проанализировал его.")

# 4. Стили для кнопок и колонок
st.markdown("""
    <style>
    .stButton>button { width: 100%; font-size: 12px; padding: 2px; }
    div[data-testid="column"] { border: 1px solid #f0f2f6; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

import streamlit as st
import google.generativeai as genai

# 1. Настройка страницы
st.set_page_config(layout="wide", page_title="Smart Reading Assistant")

# Проверка наличия ключа в Secrets
if "GEMINI_API_KEY" not in st.secrets:
    st.error("⚠️ Ключ не найден в Secrets! Добавь GEMINI_API_KEY в настройках Streamlit Cloud.")
    st.stop()

# Настройка Gemini
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

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
        words = user_text.split()
        
        # Группируем кнопки по 6 в ряд, чтобы не было "водопада"
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
        
        with st.spinner('Gemini думает...'):
            try:
                prompt = f"""
                Ты учитель. Переведи слово '{st.session_state.selected_word}' на русский.
                Объясни его роль в предложении: '{user_text}'.
                Пиши кратко.
                """
                response = model.generate_content(prompt)
                st.write(response.text)
            except Exception as e:
                st.error("Проблема с запросом к ИИ.")
        
        if st.button("Очистить"):
            st.session_state.selected_word = None
            st.rerun()
    else:
        st.info("Нажми на слово слева.")

# Стили (делаем кнопки красивыми)
st.markdown("""
    <style>
    .stButton>button { width: 100%; font-size: 14px; margin-bottom: 5px; border-radius: 8px; }
    div[data-testid="column"] { border: 1px solid #f0f2f6; padding: 15px; border-radius: 12px; background-color: #fafafa; }
    </style>
    """, unsafe_allow_html=True)

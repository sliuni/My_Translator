import streamlit as st
import google.generativeai as genai

# 1. Настройка страницы
st.set_page_config(layout="wide", page_title="Smart Reading AI")

# Проверка ключа (уже должен работать через твой Secrets)
if "GEMINI_API_KEY" not in st.secrets:
    st.error("⚠️ Ключ не найден! Проверь настройки Secrets в Streamlit.")
    st.stop()

# Инициализация Gemini
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# Память для кликов
if "selected_word" not in st.session_state:
    st.session_state.selected_word = None

st.title("Smart Reading Assistant 📖")

# 2. Колонки
col_left, col_right = st.columns([6, 4])

with col_left:
    st.header("Твой текст")
    user_text = st.text_area("Вставь текст (немецкий, английский и др.):", 
                              placeholder="Ich lerne Python каждый день...",
                              height=200)
    
    if user_text:
        st.write("### Нажми на слово для разбора:")
        
        # Разбиваем текст на слова
        words = user_text.split()
        
        # Чтобы не было "водопада", используем "плитку" из кнопок
        # Делаем сетку (например, по 5 слов в строке)
        row_size = 5
        for i in range(0, len(words), row_size):
            cols = st.columns(row_size)
            row_words = words[i:i + row_size]
            for j, word in enumerate(row_words):
                # Очищаем слово от мусора
                clean_word = word.strip(".,!?;:()\"")
                if cols[j].button(clean_word, key=f"btn_{i+j}"):
                    st.session_state.selected_word = clean_word

with col_right:
    st.header("Разбор от Gemini ✨")
    st.write("---")
    
    if st.session_state.selected_word:
        st.info(f"Выбрано слово: **{st.session_state.selected_word}**")
        
        with st.spinner('ИИ анализирует...'):
            try:
                # Промпт для ИИ
                prompt = f"""
                Ты профессиональный лингвист. 
                1. Переведи слово '{st.session_state.selected_word}' на русский.
                2. Объясни его грамматику (падеж, время, род и т.д.) в предложении: '{user_text}'.
                3. Дай еще один простой пример с этим словом.
                Пиши кратко и понятно.
                """
                response = model.generate_content(prompt)
                st.write(response.text)
            except Exception as e:
                st.error("Ошибка при получении ответа. Возможно, превышены лимиты или ключ не активен.")
        
        if st.button("Очистить"):
            st.session_state.selected_word = None
            st.rerun()
    else:
        st.write("Нажми на любое слово слева, и я объясню его значение и грамматику.")

# 3. Красивое оформление
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background-color: #f0f2f6;
        border: 1px solid #d1d5db;
        transition: 0.3s;
    }
    .stButton>button:hover {
        border-color: #ff4b4b;
        color: #ff4b4b;
    }
    div[data-testid="column"] {
        padding: 20px;
        background-color: #fafafa;
        border-radius: 15px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

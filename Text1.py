import streamlit as st
from deep_translator import GoogleTranslator

st.title("Reading Mode 📖")
st.subheader("Наведи на слово или нажми, чтобы перевести")

# Ввод текста
input_text = st.text_area("Вставь текст:", "Python is a powerful programming language.")

if input_text:
    words = input_text.split()
    
    # Создаем пустую строку для нашего "умного" текста
    annotated_text = ""
    
    st.write("---")
    
    # Рисуем интерфейс: каждое слово — это ссылка, которая не уводит на другой сайт,
    # а просто реагирует на нажатие внутри Streamlit
    cols = st.columns(len(words) if len(words) < 10 else 10) # Ограничим колонки для красоты
    
    for index, word in enumerate(words):
        # Чистим слово от знаков препинания для точного перевода
        clean_word = word.strip(".,!?;:()")
        
        if st.button(word, key=f"w_{index}", help="Нажми, чтобы перевести"):
            translation = GoogleTranslator(source='auto', target='ru').translate(clean_word)
            st.sidebar.info(f"**{clean_word}** -> {translation}")

st.sidebar.title("Словарь текущей сессии")
st.sidebar.write("Здесь будут появляться переводы нажатых слов.")



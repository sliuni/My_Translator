import streamlit as st
from deep_translator import GoogleTranslator

# Заголовок страницы
st.title("🌍 Мой личный Переводчик")
st.subheader("Made by VvodySliuni")

# Окно для ввода текста
text_to_translate = st.text_area("Введите текст на английском:", "Hello, how are you?")

# Кнопка для перевода
if st.button("Перевести"):
    if text_to_translate:
        # Логика перевода
        translated = GoogleTranslator(source='auto', target='ru').translate(text_to_translate)
        
        # Вывод результата в красивой рамке
        st.success(f"Результат: {translated}")
    else:
        st.warning("Сначала введите текст!")

st.info("Это приложение работает на твоем компьютере как локальный сайт.")
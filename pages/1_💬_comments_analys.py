import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report
import joblib
import os

if 'df' not in st.session_state:
    st.warning("Пожалуйста, загрузите файл на главной странице!")
    st.stop()

df = st.session_state['df']

# Функция для обучения модели
def train_model(data):
    X_train, X_test, y_train, y_test = train_test_split(data['comment'], data['label'], test_size=0.2, random_state=42)
    model = make_pipeline(TfidfVectorizer(), MultinomialNB())
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    st.text("Classification Report:")
    st.text(classification_report(y_test, y_pred, zero_division=0))
    joblib.dump(model, 'sentiment_model.pkl')
    return model

# Функция для классификации комментариев
def classify_comments(model, comments):
    predictions = model.predict(comments)
    classified_data = pd.DataFrame({'comment': comments, 'label': predictions})
    return classified_data

# Streamlit UI
st.title("Классификация комментариев")
st.markdown("##")

# Проверка на наличие обученной модели
model = None
model_path = 'sentiment_model.pkl'

# Загрузка файла с размеченными данными для обучения модели
training_data = df.copy()

# Переименование и очистка данных
training_data.columns = training_data.columns.str.strip()  # Убираем пробелы вокруг имен столбцов

# Загрузка обученной модели (если уже обучена ранее)
if os.path.exists(model_path):
    model = joblib.load(model_path)

# Загрузка файла с комментариями для классификации
new_data = df.copy()
new_data = new_data.drop(columns=['ID_Client', 'Имя', 'Фамилия', 'Email', 'Телефон', 'Дата', 'Услуги', 'Цена'])
new_data = new_data.dropna()
if 'comment' not in new_data.columns:
    st.error("В файле отсутствует столбец 'comment'. Пожалуйста, проверьте структуру данных.")
    st.write(new_data.columns)
    st.stop()
# Переименование и очистка данных
new_data.columns = new_data.columns.str.strip()  # Убираем пробелы вокруг имен столбцов

    
if model:
    # Классификация комментариев
    classified_data = classify_comments(model, new_data['comment'])
        
    # Разделение на категории
    positive_comments = new_data[new_data['label'] == 1]
    neutral_comments = new_data[new_data['label'] == 0]
    negative_comments = new_data[new_data['label'] == -1]

    percent_pos = round((100 * positive_comments.shape[0] / new_data.shape[0]), 1)
    percent_neu = round((100 * neutral_comments.shape[0] / new_data.shape[0]), 1)
    percent_neg = round((100 * negative_comments.shape[0] / new_data.shape[0]), 1)
    

    col1, col2, col3 = st.columns(3)
    with col1:
        # Вывод результатов
        st.subheader(f"Процент положительных комментариев {percent_pos}%")

    with col2:
        st.subheader(f"Процент нейтральных комментариев {percent_neu}%")

    with col3:
        st.subheader(f"Процент негативных комментариев {percent_neg}%")

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Вывод результатов
        st.subheader("Положительные комментарии")
        st.dataframe(positive_comments[['comment']], width=700)
    with col2:
        st.subheader("Нейтральные комментарии")
        st.dataframe(neutral_comments[['comment']], width=700)
    with col3:
        st.subheader("Негативные комментарии")
        st.dataframe(negative_comments[['comment']], width=700)
else:
    st.write("Модель не обучена. Загрузите файл с размеченными данными для обучения модели.")

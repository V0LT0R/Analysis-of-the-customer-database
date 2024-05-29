import streamlit as st
import pandas as pd
from langdetect import detect
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import spacy
import pickle

# Загрузка данных
df2 = pd.read_excel('./input_data/review.xlsx')
df = df2.copy()
df.drop(columns=['СoolServis, автосервис'], inplace=True)
df = df.rename(columns = {'с+A1:B23татус комментариев' : 'sentiment'})
df.dropna(inplace=True)
# Удаление строк с отсутствующими значениями меток классов
df.dropna(subset=['sentiment'], inplace=True)



# Определение языка комментариев
def detect_language(text):
    try:
        return detect(text)
    except:
        return 'unknown'

df['language'] = df['Комментарии'].apply(detect_language)

# Подсчет количества комментариев на казахском языке
kazakh_comments_count = df[df['language'] == 'kk'].shape[0]

# Удаление комментариев на казахском языке
df = df[df['language'] != 'kk']

# Подготовка данных для обучения
df['label'] = df['sentiment'].map({'POSITIVE': 1, 'NEGATIVE': -1, 'NEUTRAL': 0})

# Создание обучающей и тестовой выборки
X = df['Комментарии']
y = df['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Загрузка модели spaCy для русского языка
nlp = spacy.load('ru_core_news_sm')

# Функция для лемматизации текста
def lemmatize_text(text):
    doc = nlp(text)
    return ' '.join([token.lemma_ for token in doc])

X_train_lemmatized = X_train.apply(lemmatize_text)
X_test_lemmatized = X_test.apply(lemmatize_text)

# Преобразование текста в TF-IDF признаки
vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train_lemmatized)
X_test_tfidf = vectorizer.transform(X_test_lemmatized)

# Обучение модели логистической регрессии
model = LogisticRegression(max_iter=1000)
model.fit(X_train_tfidf, y_train)

# Оценка модели
y_pred = model.predict(X_test_tfidf)
report = classification_report(y_test, y_pred, target_names=['NEGATIVE', 'NEUTRAL', 'POSITIVE'])
print(report)

# Сохранение модели и векторизатора
with open('sentiment_model.pkl', 'wb') as f:
    pickle.dump((vectorizer, model), f)

# Функция для предсказания тональности
def get_sentiment(text):
    lemmatized_text = lemmatize_text(text)
    vectorized_text = vectorizer.transform([lemmatized_text])
    sentiment = model.predict(vectorized_text)[0]
    if sentiment == 1:
        return 'POSITIVE'
    elif sentiment == -1:
        return 'NEGATIVE'
    else:
        return 'NEUTRAL'

df['sentiment'] = df['Комментарии'].apply(get_sentiment)

# Разделение данных на три таблицы по полярности
positive_comments = df[df['sentiment'] == 'POSITIVE']
neutral_comments = df[df['sentiment'] == 'NEUTRAL']
negative_comments = df[df['sentiment'] == 'NEGATIVE']

# Вывод данных с использованием Streamlit
st.title('Анализ комментариев')

st.write(f'Количество комментариев на казахском языке: {kazakh_comments_count}')

st.header('Положительные комментарии')
st.dataframe(positive_comments)

st.header('Нейтральные комментарии')
st.dataframe(neutral_comments)

st.header('Отрицательные комментарии')
st.dataframe(negative_comments)

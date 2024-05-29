# Анализ клиентской базы данных сервисной компании

Этот проект является частью дипломной работы и представляет собой веб-приложение для анализа клиентской базы данных сервисной компании. Веб-приложение разработано с использованием Streamlit и включает в себя анализ данных с помощью библиотек Pandas, Plotly Express и Scikit-learn.

## Описание проекта

Приложение позволяет пользователю загружать файл с данными, анализировать эти данные и визуализировать результаты. Пользователь может выбирать, какие данные отображать в таблицах и графиках, а также выполнять различные операции анализа данных.

## Функциональные возможности

- Загрузка файла с данными (CSV, Excel)
- Отображение данных в виде таблиц
- Визуализация данных с использованием графиков (Plotly Express)
- Анализ данных с использованием методов машинного обучения (Scikit-learn)

## Установка и запуск проекта

### Требования

- Python 3.7 или выше
- Установленные зависимости (см. файл `requirements.txt`)

### Установка зависимостей

1. Клонируйте репозиторий проекта:

```bash
git clone https://github.com/V0LT0R/DIPLOMKA_COLLEGE.git
```

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

### Запуск проекта

Запустите Streamlit приложение:

```bash
streamlit run app.py
```

Перейдите по адресу `http://localhost:8501` в вашем веб-браузере, чтобы взаимодействовать с приложением.

## Использование приложения

1. Загрузите файл с данными, выбрав его с помощью кнопки "Browse files".
2. После загрузки данных, выберите параметры для отображения в таблицах и графиках.
3. Используйте предоставленные инструменты для анализа данных, включая фильтрацию, сортировку и визуализацию.


## Библиотеки и технологии

- [Streamlit](https://streamlit.io/) - для создания веб-приложения
- [Pandas](https://pandas.pydata.org/) - для работы с данными
- [Plotly Express](https://plotly.com/python/plotly-express/) - для визуализации данных
- [Scikit-learn](https://scikit-learn.org/stable/) - для машинного обучения и анализа данных

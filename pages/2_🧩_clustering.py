import pandas as pd
import streamlit as st
import plotly.express as px
import extra_streamlit_components as stx
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
import plotly.graph_objs as go
import plotly.figure_factory as ff

st.set_page_config(page_title="Analysis", page_icon="🔥", layout="wide")

if 'df' not in st.session_state:
    st.warning("Пожалуйста, загрузите файл на главной странице!")
    st.stop()

df = st.session_state['df']

st.sidebar.header("Please Filter Here:")
customer_year = st.sidebar.multiselect(
    "Select the year:",
    options=df["Дата"].dt.year.unique(),
    default=df["Дата"].dt.year.unique()
)
df_filtered_2graph = df[df['Дата'].dt.year.isin(customer_year)]
# Check if the dataframe is empty:
if df_filtered_2graph.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop()  # This will halt the app from further execution.
df = df_filtered_2graph

# ---- MAINPAGE ----
st.title("🧩 Clustering")
st.markdown("##")
st.markdown("""---""")

visits = df.groupby('ID_Client').size().reset_index(name='Количество посещений')

# Иерархическая кластеризация
X = visits[['Количество посещений']].values

# Создание кластеров
n_clusters = 4
cluster = AgglomerativeClustering(n_clusters=n_clusters, metric='euclidean', linkage='ward')
visits['Кластер'] = cluster.fit_predict(X)

# Определение меток кластеров
cluster_labels = {
    0: 'Постоянные посетители', 
    1: 'Постоянные посетители', 
    2: 'Средние посетители', 
    3: 'Частые посетители'
}

# Центры кластеров для аннотаций
cluster_centers = visits.groupby('Кластер')['Количество посещений'].mean().reset_index()
label_positions = {i: cluster_centers.loc[cluster_centers['Кластер'] == i, 'Количество посещений'].values[0] for i in range(n_clusters)}

# Визуализация кластеров с Plotly
fig_clusters = px.scatter(
    visits, x='ID_Client', y='Количество посещений', color='Кластер',
    title='',
    labels={'ID_Client': 'ID Клиента', 'Количество посещений': 'Количество посещений'}
)

# Добавление меток кластерам
for cluster_num, label in cluster_labels.items():
    cluster_data = visits[visits['Кластер'] == cluster_num]
    fig_clusters.add_annotation(
        x=cluster_data['ID_Client'].mean(), 
        y=label_positions[cluster_num], 
        text=label, 
        showarrow=False, 
        font=dict(size=12, color="black"), 
        bgcolor="white", 
        opacity=0.7
    )
col1, col2 = st.columns([1, 1], gap="medium")
with col1:
    st.subheader("Иерархическая Кластеризация")
    st.plotly_chart(fig_clusters, use_container_width=True)

customer_data = df.groupby('ID_Client').agg(
    Количество_посещений=('ID_Client', 'size'),
    Средний_чек=('Цена', 'mean')
).reset_index()
# Применение KMeans для кластеризации
X = customer_data[['Количество_посещений', 'Средний_чек', 'ID_Client']].values
n_clusters = 5
km = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=300, n_init=10, random_state=0)
km.fit(X)
labels = km.labels_
centroids = km.cluster_centers_

customer_data['labels'] = labels

# Визуализация кластеров
trace1 = go.Scatter3d(
    x=customer_data['Количество_посещений'],
    y=customer_data['Средний_чек'],
    z=customer_data['ID_Client'],
    mode='markers',
    marker=dict(
        color=customer_data['labels'],
        size=10,
        line=dict(
            color=customer_data['labels'],
            width=12
        ),
        opacity=0.8
    )
)

df_change = [trace1]
layout = go.Layout(
    title=' ',
    margin=dict(l=0, r=0, b=0, t=0),
    scene=dict(
        xaxis=dict(title='Количество посещений'),
        yaxis=dict(title='Средний чек'),
        zaxis=dict(title='ID клиента')
    )
)

fig = go.Figure(data=df_change, layout=layout)
with col2:
    st.subheader("3D Кластеризация")
    st.plotly_chart(fig, use_container_width=True)

# Подготовка данных для ABC и XYZ анализа
customer_data = df.groupby('ID_Client').agg(
    Количество_посещений=('ID_Client', 'size'),
    Общая_сумма=('Цена', 'sum'),
    Средний_чек=('Цена', 'mean'),
    Вариабельность_покупок=('Цена', 'std')
).reset_index()

# ---- ABC-АНАЛИЗ ----
# Сортировка клиентов по общей сумме покупок
customer_data = customer_data.sort_values(by='Общая_сумма', ascending=False)

# Расчет кумулятивной суммы и процентиля
customer_data['Кумулятивная_сумма'] = customer_data['Общая_сумма'].cumsum()
total_sum = customer_data['Общая_сумма'].sum()
customer_data['Процентиль'] = customer_data['Кумулятивная_сумма'] / total_sum

# Классификация клиентов по ABC
def classify_abc(row):
    if row['Процентиль'] <= 0.8:
        return 'A'
    elif row['Процентиль'] <= 0.95:
        return 'B'
    else:
        return 'C'

customer_data['ABC'] = customer_data.apply(classify_abc, axis=1)

# ---- XYZ-АНАЛИЗ ----
# Вариабельность покупок
customer_data['Вариабельность_покупок'].fillna(0, inplace=True)

# Классификация клиентов по XYZ
def classify_xyz(row):
    if row['Вариабельность_покупок'] <= customer_data['Вариабельность_покупок'].quantile(0.3):
        return 'X'
    elif row['Вариабельность_покупок'] <= customer_data['Вариабельность_покупок'].quantile(0.9):
        return 'Y'
    else:
        return 'Z'

customer_data['XYZ'] = customer_data.apply(classify_xyz, axis=1)

# ---- ВИЗУАЛИЗАЦИЯ ----
st.title("ABC-XYZ Analysis")
st.markdown("##")
st.markdown('---')

col1, col2 = st.columns([1, 1], gap="medium")
with col1:
    # ABC-аналіз таблиця
    st.subheader("ABC Analysis")
    st.write(customer_data[['ID_Client', 'Общая_сумма', 'ABC']], use_container_width=True)
with col2:
    # XYZ-аналіз таблиця
    st.subheader("XYZ Analysis")
    st.write(customer_data[['ID_Client', 'Вариабельность_покупок', 'XYZ']], use_container_width=True)

col1, col2 = st.columns([1, 1], gap="medium")
with col1:
    # Визуализация распределения ABC
    st.subheader("ABC Распределение")
    abc_distribution = customer_data['ABC'].value_counts().reset_index()
    abc_distribution.columns = ['Category', 'Count']
    st.bar_chart(abc_distribution.set_index('Category'))
with col2:
    # Визуализация распределения XYZ
    st.subheader("XYZ Распределение")
    xyz_distribution = customer_data['XYZ'].value_counts().reset_index()
    xyz_distribution.columns = ['Category', 'Count']
    st.bar_chart(xyz_distribution.set_index('Category'))

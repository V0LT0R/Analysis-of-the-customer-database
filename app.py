import pandas as pd
import streamlit as st
import plotly.express as px
import extra_streamlit_components as stx

st.set_page_config(page_title="Analysis", page_icon="🔥", layout="wide")

services = [
    "Техническое_обслуживание",
    "Диагностика_двигателя",
    "Замена_масла_и_фильтров",
    "Ремонт_подвески",
    "Обслуживание_тормозной_системы",
    "Кузовной_ремонт_и_покраска",
    "Шиномонтажные_услуги",
    "Ремонт_электрических_систем",
    "Установка_и_настройка_дополнительного_оборудования"
]
# ---- MAINPAGE ----
st.title(":bar_chart: Analysis")
st.markdown("##")

# ---- READ EXCEL ----
@st.cache_data
def get_data_from_csv(file):
    df = pd.read_csv(file)
    df['Дата'] = pd.to_datetime(df['Дата'])  # Преобразование столбца "Дата" в datetime
    return df

uploaded_file = st.file_uploader("Выберите файл", type=["csv", "txt", "xlsx"])
if uploaded_file is not None:
    df = get_data_from_csv(uploaded_file)
    st.session_state['df'] = df  # Сохранение данных в состояние сессии

if 'df' not in st.session_state:
    st.warning("Пожалуйста, загрузите файл!")
    st.stop()

df = st.session_state['df']

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
selected_services = st.sidebar.multiselect(
    "Select the Service:",
    options=services,
    default=services[0]
)

customer_year = st.sidebar.multiselect(
    "Select the year:",
    options=df["Дата"].dt.year.unique(),
    default=df["Дата"].dt.year.unique()
)

# Функция для фильтрации данных по выбранным услугам
def filter_services(df, services):
    # Фильтрация строк, которые содержат хотя бы одну из выбранных услуг
    mask = df['Услуги'].apply(lambda x: any(service in x for service in services))
    return df[mask]

# Применяем фильтрацию
df_filtered = filter_services(df[df['Дата'].dt.year.isin(customer_year)], selected_services)
df_filtered_2graph = df[df['Дата'].dt.year.isin(customer_year)]
# Check if the dataframe is empty:
if df_filtered.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop()  # This will halt the app from further execution.

# TOP KPI's
total_sales = int(df_filtered["Цена"].sum())
average_sale_by_transaction = round(df_filtered["Цена"].mean(), 2)

left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"KZT ₸ {total_sales:,}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"KZT ₸ {average_sale_by_transaction}")

st.markdown("""---""")

col1, col2 = st.columns([1, 1], gap="medium")

# График зависимости покупок от времени
with col1:
    st.subheader("Зависимость покупок от времени")
    df_filtered['Month'] = df_filtered['Дата'].dt.to_period('M').astype(str)
    sales_over_time = df_filtered.groupby('Month')['Цена'].sum().reset_index()
    fig_sales_over_time = px.line(sales_over_time, x='Month', y='Цена', title='')
    fig_sales_over_time.update_layout(
        xaxis_title='Month',
        yaxis_title='Цена',
        xaxis_title_font=dict(size=24),  
        yaxis_title_font=dict(size=24),  
        xaxis_tickfont=dict(size=14),    
        yaxis_tickfont=dict(size=14)     
    )
    st.plotly_chart(fig_sales_over_time, use_container_width=True)

# График прибыльности каждой из услуг
with col2:
    st.subheader("Прибыльность каждой из услуг")
    # Разделяем строки с услугами, чтобы каждая услуга была в отдельной строке
    df_services_split = df_filtered_2graph.drop('Услуги', axis=1).join(
        df_filtered_2graph['Услуги'].str.split(',', expand=True).stack().reset_index(level=1, drop=True).rename('Услуги'))
    # Фильтруем только выбранные услуги
    df_services_split = df_services_split[df_services_split['Услуги'].isin(services)]
    profit_by_service = df_services_split.groupby('Услуги')['Цена'].sum().reset_index()
    fig_profit_by_service = px.bar(profit_by_service, orientation='h', y='Услуги', x='Цена', title='')
    fig_profit_by_service.update_layout(
        xaxis_tickangle=0, 
        # margin=dict(l=20, r=20, t=50, b=100),
        xaxis_title_font=dict(size=24),  
        yaxis_title_font=dict(size=24),  
        xaxis_tickfont=dict(size=14),    
        yaxis_tickfont=dict(size=14)    
        )
    st.plotly_chart(fig_profit_by_service, use_container_width=True)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .css-18e3th9 {padding: 2rem 1rem;}
            .css-1d391kg {padding: 2rem 1rem;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

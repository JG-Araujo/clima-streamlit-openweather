import streamlit as st
import pandas as pd
cities_filter = []
def filtros_sidebar(df: pd.DataFrame):
    st.sidebar.header("Filtros (Drill-down)")
    global cities_filter
# filtro Cidade
    city_option = df["name"].tolist()
    cities_filter = st.sidebar.multiselect(
        "Cidades",
        options=city_option,
        default=[]
    )


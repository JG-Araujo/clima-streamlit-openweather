import streamlit as st
import pandas as pd
import api_clima as ac
def filtros_sidebar(df: pd.DataFrame):
    # st.sidebar.header("Filtros (Drill-down)")
    global cities_filter
# filtro Cidade
    city_option = df["name"].tolist() 
    cities_filter = st.sidebar.multiselect(
        "Cidades",
        options=city_option,
        max_selections=1,
        default=[]
    )

def previsao(cidade: list) -> pd.DataFrame:
    lat,lon = ac.obter_coordenadas(cidade)
    clima_atual = ac.obter_clima_atual(lat, lon)
    dados = {'Cidade': [cidade],
             'Temperatura': [clima_atual['temperatura']],
             'Sensação Térmica': [clima_atual['sensacao']],
             'Umidade': [clima_atual['umidade']],
             'Descrição': [clima_atual['descricao']],
             'Velocidade do Vento': [clima_atual['vento']]

        }
    df_clima = pd.DataFrame(dados)
    return df_clima 



def aplicar_filtros(df_base: pd.DataFrame) -> pd.DataFrame:
    df_f = df_base.copy()
    if cities_filter:
        df_f = df_f[df_f["name"].isin(cities_filter)]
    return df_f


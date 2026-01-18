import streamlit as st
import pandas as pd
import json
from servicos_api import api_clima as ac

# --- 1. CACHE DE DADOS ---
@st.cache_data
def carregar_dados_globais():
    try:
        with open('city.list.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        
        if 'coord' in df.columns:
            coords = pd.json_normalize(df['coord'])
            df = df.drop(columns=['coord']).join(coords)
            
        return df
    except FileNotFoundError:
        st.error("Arquivo 'city.list.json' não encontrado.")
        return pd.DataFrame()

# --- 2. SIDEBAR ---
def renderizar_filtros(df_completo: pd.DataFrame):
    st.sidebar.header("Filtros")
    
    if df_completo.empty:
        return None

    paises = sorted(df_completo['country'].unique())
    pais_selecionado = st.sidebar.selectbox("1. Selecione o País:", options=paises)
    
    df_cidades_pais = df_completo[df_completo['country'] == pais_selecionado]
    df_cidades_pais = df_cidades_pais.sort_values(by='name')
    
    cidade_nome = st.sidebar.selectbox(
        "2. Selecione a Cidade:",
        options=df_cidades_pais['name'].unique()
    )
    
    cidade_dados = df_cidades_pais[df_cidades_pais['name'] == cidade_nome].iloc[0]
    return cidade_dados

# --- 3. PREVISÃO GERAL ---
def previsao(cidade_dados) -> pd.DataFrame:
    lat = cidade_dados['lat']
    lon = cidade_dados['lon']
    nome = cidade_dados['name']
    
    # Chama as APIs
    clima_atual = ac.obter_clima_atual(lat, lon)
    clima_dias = ac.obter_previsao(lat, lon)
    poluicao = ac.obter_poluicao_ar(lat, lon)
    
    dados = {
        'Cidade': [nome],
        'Temperatura': [clima_atual.get('temperatura', 0)],
        'Sensação Térmica': [clima_atual.get('sensacao', 0)],
        'Umidade': [clima_atual.get('umidade', 0)],
        'Descrição': [clima_atual.get('descricao', 'N/A')],
        'Velocidade do Vento': [clima_atual.get('vento', 0)],
        'Previsão': [clima_dias],  
        'Poluição do Ar': [poluicao]
    }
    
    return pd.DataFrame(dados)

def formatar_previsao_grafico(lista_previsao):
    """
    Formata a previsão para gráfico de linha (5 dias).
    """
    df = pd.DataFrame(lista_previsao)

    df['data'] = pd.to_datetime(df['data'])
    df['temperatura'] = df['temperatura']

    return df[['data', 'temperatura']]


def formatar_poluicao_df(dados_poluicao: dict) -> pd.DataFrame:
    """
    Formata os dados de poluição para uso em gráficos.
    """
    return pd.DataFrame({
        "Poluente": ["AQI", "PM2.5", "PM10"],
        "Valor": [
            dados_poluicao.get("aqi", 0),
            dados_poluicao.get("pm2_5", 0),
            dados_poluicao.get("pm10", 0)
        ]
    })
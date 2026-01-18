import streamlit as st
import pandas as pd
import json
# Supondo que servicos_api.api_clima tenha a função obter_clima_atual(lat, lon)
from servicos_api import api_clima as ac

# --- 1. CACHE DE DADOS (Performance Extrema) ---
@st.cache_data
def carregar_dados_globais():
    """
    Carrega o JSON gigante apenas uma vez e deixa na memória RAM.
    Tenta ler de um arquivo 'city.list.json' na raiz.
    """
    try:
        # Se você tiver o arquivo JSON descompactado:
        with open('city.list.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        
        # Otimização: Normalizar coordenadas se estiverem aninhadas
        # O JSON da OpenWeather geralmente vem como dict dentro de 'coord'
        if 'coord' in df.columns:
            coords = pd.json_normalize(df['coord'])
            df = df.drop(columns=['coord']).join(coords)
            
        return df
    except FileNotFoundError:
        st.error("Arquivo 'city.list.json' não encontrado. Por favor, adicione o arquivo na pasta.")
        return pd.DataFrame()

# --- 2. SIDEBAR COM CASCATA (País -> Cidade) ---
def renderizar_filtros(df_completo: pd.DataFrame):
    """
    Renderiza os filtros e RETORNA a cidade selecionada (Series do Pandas).
    """
    st.sidebar.header("Filtros")
    
    if df_completo.empty:
        return None

    # Passo A: Selecionar País
    # Sorted para ficar em ordem alfabética
    paises = sorted(df_completo['country'].unique())
    pais_selecionado = st.sidebar.selectbox("1. Selecione o País:", options=paises)
    
    # Passo B: Filtrar cidades apenas daquele país (Muito rápido no Pandas)
    df_cidades_pais = df_completo[df_completo['country'] == pais_selecionado]
    df_cidades_pais = df_cidades_pais.sort_values(by='name')
    
    # Passo C: Selecionar Cidade
    cidade_nome = st.sidebar.selectbox(
        "2. Selecione a Cidade:",
        options=df_cidades_pais['name'].unique()
    )
    
    # Retorna a LINHA completa do DataFrame correspondente à escolha
    # (Assim já teremos lat e lon sem precisar buscar de novo)
    cidade_dados = df_cidades_pais[df_cidades_pais['name'] == cidade_nome].iloc[0]
    
    return cidade_dados

# --- 3. PREVISÃO OTIMIZADA ---
def previsao(cidade_dados) -> pd.DataFrame:
    """
    Recebe a LINHA do dataframe (com lat/lon já prontos).
    Economiza a chamada de API de Geocoding.
    """
    # Pegamos lat e lon direto do JSON carregado (mais rápido e preciso)
    lat = cidade_dados['lat']
    lon = cidade_dados['lon']
    nome = cidade_dados['name']
    
    # Chama apenas a API de clima
    clima_atual = ac.obter_clima_atual(lat, lon)
    clima_dias = ac.obter_previsao(lat, lon)
    poluicao = ac.obter_poluicao_ar(lat, lon)
    
    # Monta o DataFrame
    dados = {
        'Cidade': [nome],
        'Temperatura': [clima_atual.get('temperatura', 0)],
        'Sensação Térmica': [clima_atual.get('sensacao', 0)],
        'Umidade': [clima_atual.get('umidade', 0)],
        'Descrição': [clima_atual.get('descricao', 'N/A')],
        'Velocidade do Vento': [clima_atual.get('vento', 0)],
        'Previsão': [clima_dias],  # Lista de previsões futuras
        'Poluição do Ar': [poluicao]
    }
    
    return pd.DataFrame(dados)
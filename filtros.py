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

# --- 4. FUNÇÃO NOVA: FORMATAR TABELA 48H ---
def formatar_previsao_48h(lista_previsao):
    """
    Recebe a lista crua da API e formata para exibição bonita de 48h.
    """
    # Pega apenas os próximos 16 registros (16 * 3h = 48h)
    dados_48h = lista_previsao[:16]
    
    df = pd.DataFrame(dados_48h)
    
    # Formatar Data (de "2026-01-18 18:00:00" para "18/01 18:00")
    df['data'] = pd.to_datetime(df['data'])
    df['Data/Hora'] = df['data'].dt.strftime('%d/%m %H:%M')
    
    # Formatar Temperatura
    df['Temperatura'] = df['temperatura'].apply(lambda x: f"{x:.1f}°C")
    
    # Formatar Descrição (Capitalizar)
    df['Condição'] = df['descricao'].str.title()
    
    # Selecionar e reordenar colunas finais
    df_final = df[['Data/Hora', 'Temperatura', 'Condição']]
    
    return df_final
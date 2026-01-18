import pandas as pd
import streamlit as st
import json

def padronizar_colunas(df: pd.DataFrame) -> pd.DataFrame:
    """Ajustes leves: tipos e colunas auxiliares."""
    df = df.copy()

    # Garantir que colunas existam (para evitar erros em datasets similares)
    colunas_esperadas = ['name', 'country']
    faltantes = [c for c in colunas_esperadas if c not in df.columns]
    if faltantes:
        st.error(f"Colunas faltantes no CSV: {faltantes}")
        st.stop()
    return df

def carregar_cidades() -> list:
    """Carrega a lista de cidades a partir de um arquivo CSV."""
    try:
        df = pd.read_json("city.list.json")
        df = padronizar_colunas(df)
        return df['name'].tolist(), df['country'].tolist(), df['coord'].tolist()
    except FileNotFoundError:
        st.error(f"Arquivo não encontrado: cities_list.csv ")
        st.stop()
    except pd.errors.EmptyDataError:
        st.error("Arquivo CSV está vazio.")
        st.stop()
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo CSV: {e}")
        st.stop()

def traduzir_aqi(aqi_valor):
    """
    Traduz o índice AQI (1-5) da OpenWeather para texto e cor.
    """
    mapa = {
        1: ("Bom", "🟢", "#00e400"),      # Verde
        2: ("Razoável", "🟡", "#ffff00"), # Amarelo
        3: ("Moderado", "🟠", "#ff7e00"), # Laranja
        4: ("Ruim", "🔴", "#ff0000"),     # Vermelho
        5: ("Muito Ruim", "🟣", "#8f3f97") # Roxo
    }
    # Retorna (Texto, Emoji, CorHex)
    return mapa.get(aqi_valor, ("Desconhecido", "❓", "#808080"))
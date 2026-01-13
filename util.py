import pandas as pd
import streamlit as st

def padronizar_colunas(df: pd.DataFrame) -> pd.DataFrame:
    """Ajustes leves: tipos e colunas auxiliares."""
    df = df.copy()

    # Garantir que colunas existam (para evitar erros em datasets similares)
    colunas_esperadas = ['name', 'country']
    faltantes = [c for c in colunas_esperadas if c not in df.columns]
    # if faltantes:
    #     st.error(f"Colunas faltantes no CSV: {faltantes}")
    #     st.stop()
    return df

def carregar_cidades() -> pd.DataFrame:
    """Carrega a lista de cidades a partir de um arquivo CSV."""
    try:
        df = pd.read_csv("cities_list.csv")
        df = padronizar_colunas(df)
        return df
    except FileNotFoundError:
    #     st.error(f"Arquivo não encontrado: cities_list.csv ")
    #     st.stop()
    # except pd.errors.EmptyDataError:
    #     st.error("Arquivo CSV está vazio.")
    #     st.stop()
    # except Exception as e:
    #     st.error(f"Erro ao carregar o arquivo CSV: {e}")
    #     st.stop()
        print("Erro ao carregar o arquivo cities_list.csv")
lista = carregar_cidades()
print(lista.head())
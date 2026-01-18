import pandas as pd
import streamlit as st

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
import pandas as pd

def tabela_clima_atual(df: pd.DataFrame) -> pd.DataFrame:
    return df[
        ['Cidade',
         'Temperatura',
         'Sensação Térmica',
         'Umidade',
         'Descrição',
         'Velocidade do Vento']
    ]

def formatar_previsao_48h(lista_previsao):
    """
    Recebe a lista crua da API e formata para exibição bonita de 48h.
    """
    # Pega apenas os próximos 16 registros (16 * 3h = 48h)
    dados_48h = lista_previsao[:16]
    
    df = pd.DataFrame(dados_48h)

    def emoji_descricao(desc):
        desc = desc.lower()
        if "chuva" in desc:
            return "🌧️"
        elif "nublado" in desc:
            return "☁️"
        elif "céu limpo" in desc:
            return "☀️"
        elif "neve" in desc:
            return "❄️"
        elif "tempestade" in desc:
            return "⛈️"
        else:
            return "🌤️"
    
    # Formatar Data (de "2026-01-18 18:00:00" para "18/01 18:00")
    df['data'] = pd.to_datetime(df['data'])
    df['Data/Hora'] = df['data'].dt.strftime('%d/%m %H:%M')
    
    # Formatar Temperatura
    df['Temperatura'] = df['temperatura'].apply(lambda x: f"{x:.1f}°C")
    
    # Formatar Descrição (Capitalizar)
    df['Condição'] = df['descricao'].apply(
        lambda x: f"{emoji_descricao(x)} {x.title()}"
    )
    
    # Selecionar e reordenar colunas finais
    df_final = df[['Data/Hora', 'Temperatura', 'Condição']]
    
    return df_final


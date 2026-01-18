import pandas as pd
import plotly.express as px

def grafico_clima_atual(df: pd.DataFrame):
    """
    Gráfico de barras com métricas do clima atual + emojis
    """

    def emoji_temperatura(valor):
        if valor < 10:
            return "❄️"
        elif valor > 30:
            return "☀️"
        else:
            return "🌤️"

    def emoji_umidade(valor):
        if valor < 30:
            return "🏜️"
        elif valor > 70:
            return "💧"
        else:
            return "🌫️"

    df_melt = df.melt(
        id_vars='Cidade',
        value_vars=['Temperatura', 'Sensação Térmica', 'Umidade'],
        var_name='Métrica',
        value_name='Valor'
    )

    # emojis por métrica
    emojis = []
    for _, row in df_melt.iterrows():
        if row["Métrica"] in ["Temperatura", "Sensação Térmica"]:
            emojis.append(f"{emoji_temperatura(row['Valor'])} {round(row['Valor'],1)}")
        else:
            emojis.append(f"{emoji_umidade(row['Valor'])} {round(row['Valor'],1)}%")

    df_melt["Label"] = emojis

    fig = px.bar(
        df_melt,
        x='Métrica',
        y='Valor',
        color='Métrica',
        text='Label',
        title=f"Clima atual em {df['Cidade'].iloc[0]}"
    )

    fig.update_traces(textfont_size=20, textposition="inside")
    fig.update_layout(showlegend=False)

    return fig

def grafico_previsao_temperatura(df_previsao: pd.DataFrame):
    """
    Gráfico de linha da previsão de temperatura
    """
    fig = px.line(
        df_previsao,
        x='data',
        y='temperatura',
        title="Previsão de Temperatura (5 dias)",
        markers=True
    )

    return fig

def grafico_poluicao_ar(df_poluicao: pd.DataFrame):

    def descricao_poluente(poluente, valor):
        if poluente == "AQI":
            if valor <= 1:
                return "🟢 Boa"
            elif valor == 2:
                return "🟡 Razoável"
            elif valor == 3:
                return "🟠 Moderada"
            elif valor == 4:
                return "🔴 Ruim"
            else:
                return "🟣 Muito Ruim"
        else:  # PM2.5 e PM10
            if valor <= 25:
                return "🟢 Boa"
            elif valor <= 50:
                return "🟡 Moderada"
            else:
                return "🔴 Ruim"

    df = df_poluicao.copy()
    df["Situação"] = df.apply(
        lambda row: descricao_poluente(row["Poluente"], row["Valor"]),
        axis=1
    )

    fig = px.bar(
        df,
        x="Poluente",
        y="Valor",
        text="Situação",
        title="Qualidade do Ar"
    )

    fig.update_traces(textposition="inside", textfont_size=20)
    return fig



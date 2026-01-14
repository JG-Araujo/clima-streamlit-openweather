import streamlit as st
import pandas as pd
import filtros as f
from util import carregar_cidades
import time

# 1. Configuração da página (título na aba do navegador)
st.set_page_config(page_title="Clima Hoje", page_icon=":sun_with_face:", layout="wide")

# 2. Título e Subtítulo na página
st.title("Clima Hoje :sun_with_face:")
st.write("Veja as métricas de clima")
st.caption("Escolha uma cidade na barra lateral para ver o clima atual e a previsão.")
# carregando lista de cidades em um DataFrame
dados = {
    'Cidade': carregar_cidades()
}
############### LER CIDADES DISPONIVEIS APENAS UMA VEZ (FAZER FUNÇÃO) ###############
df = pd.DataFrame(dados)
opcoes = ['selecione uma cidade'] + df['Cidade'].unique().tolist()

# 4. Barra Lateral (Sidebar) para Filtros
st.sidebar.header("Filtros")
cidade_selecionada = st.sidebar.selectbox(
    "selecione uma cidade",
    options=opcoes,
)
# Filtrando o DataFrame baseado na escolha
if cidade_selecionada == 'selecione uma cidade':
    st.info("Por favor, selecione uma cidade para ver o clima.")
else:
    df_filtrado = f.previsao(cidade_selecionada)

   # Métricas do dia atual (primeira linha do df FILTRADO)
    col1, col2, col3 = st.columns(3)
    cidade = df_filtrado['Cidade'][0]
    Temp = df_filtrado["Temperatura"][0]
    Sensacao = df_filtrado["Sensação Térmica"][0]
    Umidade = df_filtrado["Umidade"][0]
    Descricao = df_filtrado["Descrição"][0]
    Vento = df_filtrado["Velocidade do Vento"][0]

    hora = time.strftime("%H:%M:%S", time.localtime())
    
    st.write(f"Atualizado às: {hora}")
    col1.metric("CIDADE", f"{cidade}") 
    col1.metric("UMIDADE", f"{int(Umidade)}%")
    
    col2.metric("TEMPERATURA",f"{int(Temp)}°C")
    col2.metric("SENSAÇÃO TÉRMICA", f"{int(Sensacao)}°C")
    
    col3.metric("DESCRIÇÃO", f"{Descricao}")
    col3.metric("VELOCIDADE DO VENTO", f"{int(Vento)} m/s")

    # # 6. Exibindo o Gráfico com Plotly
    # st.subheader(f"Gráfico de Vendas - {categoria_selecionada}")
    # fig = px.bar(df_filtrado, x='Produto', y='Vendas', color='Produto', title="Vendas por Produto")
    # st.plotly_chart(fig, use_container_width=True)
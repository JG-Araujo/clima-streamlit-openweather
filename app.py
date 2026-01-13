import streamlit as st
import pandas as pd
import plotly.express as px
import filtros as f
from util import carregar_cidades

# 1. Configuração da página (título na aba do navegador)
st.set_page_config(page_title="Clima Hoje", page_icon=":sun_with_face:", layout="wide")
# 2. Título e Subtítulo na página
st.title("Clima Hoje :sun_with_face:")
st.write("Veja as métricas de clima")
# 3. Criando dados de exemplo (Simulando um Excel/CSV)
dados = {
    'Produto': ['Notebook', 'Mouse', 'Teclado', 'Monitor', 'Cadeira', 'Headset'],
    'Vendas': [15000, 2000, 3500, 8000, 5000, 1200],
    'Quantidade': [5, 40, 20, 10, 8, 15],
    'Categoria': ['Eletrônicos', 'Acessórios', 'Acessórios', 'Eletrônicos', 'Móveis', 'Acessórios']
}
df = pd.DataFrame(dados)
cidades = carregar_cidades()

# 4. Barra Lateral (Sidebar) para Filtros
f.filtros_sidebar(cidades)

# Filtrando o DataFrame baseado na escolha
categoria_selecionada = st.sidebar.selectbox(
    "Selecione a Categoria",
    options=df["Categoria"].unique()
)

# 5. Exibindo Métricas (KPIs)
col1, col2 = st.columns(2)
df_filtrado = df[df["Categoria"] == categoria_selecionada]
total_vendas = df_filtrado['Vendas'].sum()
total_qtd = df_filtrado['Quantidade'].sum()

col1.metric("Faturamento Total", f"R$ {total_vendas:,.2f}")
col2.metric("Itens Vendidos", total_qtd)

# 6. Exibindo o Gráfico com Plotly
st.subheader(f"Gráfico de Vendas - {categoria_selecionada}")
fig = px.bar(df_filtrado, x='Produto', y='Vendas', color='Produto', title="Vendas por Produto")
st.plotly_chart(fig, use_container_width=True)

# 7. Exibindo os dados brutos (opcional)
if st.checkbox("Mostrar tabela de dados"):
    st.dataframe(df_filtrado)
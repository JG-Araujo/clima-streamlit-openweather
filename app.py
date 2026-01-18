import streamlit as st
import filtros as f
import time

# 1. Configuração da página
st.set_page_config(page_title="Clima Hoje", page_icon="🌤️", layout="wide")

st.title("Clima Hoje 🌤️")
st.write("Veja as métricas de clima em tempo real.")
st.caption("Use a barra lateral para filtrar por País e Cidade.")

# 2. Carregar o banco de dados gigante (Acontece 1 vez e fica em cache)
with st.spinner("Carregando banco de dados de cidades..."):
    df_global = f.carregar_dados_globais()

# 3. Renderizar Sidebar e Capturar a escolha do usuário
# A função retorna os dados da cidade escolhida ou None
cidade_escolhida = f.renderizar_filtros(df_global)

# 4. Lógica de Exibição
if cidade_escolhida is None:
    st.info("👈 O banco de dados está vazio ou não foi carregado.")
    
elif isinstance(cidade_escolhida, str): 
    # Fallback caso algo dê errado no filtro e não retorne a linha
    st.warning("Selecione uma cidade válida.")
    
else:
    # Se temos uma cidade escolhida, buscamos a previsão
    # Passamos os dados completos (que incluem lat/lon)
    try:
        df_filtrado = f.previsao(cidade_escolhida)
        
        # Métricas
        col1, col2, col3 = st.columns(3)
        
        # Usamos .iloc[0] para pegar o valor escalar (evita erros de Series)
        cidade_nome = df_filtrado['Cidade'].iloc[0]
        temp = df_filtrado["Temperatura"].iloc[0]
        sensacao = df_filtrado["Sensação Térmica"].iloc[0]
        umidade = df_filtrado["Umidade"].iloc[0]
        descricao = df_filtrado["Descrição"].iloc[0]
        vento = df_filtrado["Velocidade do Vento"].iloc[0]
        previsao = df_filtrado["Previsão"].iloc[0]
        poluicao = df_filtrado["Poluição do Ar"].iloc[0]

        hora = time.strftime("%H:%M:%S", time.localtime())
        st.write(f"Última atualização: {hora}")
        
        col1.metric("CIDADE", f"{cidade_nome}")
        col1.metric("UMIDADE", f"{int(umidade)}%")
        
        col2.metric("TEMPERATURA", f"{int(temp)}°C")
        col2.metric("SENSAÇÃO TÉRMICA", f"{int(sensacao)}°C")
        
        col3.metric("DESCRIÇÃO", f"{descricao.title()}")
        col3.metric("VENTO", f"{vento} m/s")
        
    except Exception as e:
        st.error(f"Erro ao buscar dados da API: {e}")
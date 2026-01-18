import streamlit as st
import filtros as f
import time
from util import traduzir_aqi # Importa a função nova

# 1. Configuração da página (Modo Wide para aproveitar espaço)
st.set_page_config(page_title="Clima Hoje", page_icon="🌤️", layout="wide")

# CSS Personalizado para deixar o título mais bonito e métricas centralizadas
st.markdown("""
<style>
    [data-testid="stMetricValue"] {
        font-size: 24px;
    }
    h1 {
        color: #FF4B4B;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

st.title("Clima Hoje 🌤️")
st.caption("Dashboard meteorológico em tempo real.")

# 2. Carregar dados (Cache)
with st.spinner("Carregando banco de dados..."):
    df_global = f.carregar_dados_globais()

# 3. Sidebar
cidade_escolhida = f.renderizar_filtros(df_global)

# 4. Lógica Principal
if cidade_escolhida is None:
    st.info("👈 O banco de dados está vazio.")
    
elif isinstance(cidade_escolhida, str): 
    st.warning("Selecione uma cidade válida.")
    
else:
    try:
        # Busca todos os dados
        df_filtrado = f.previsao(cidade_escolhida)
        
        # --- Extração de Dados ---
        cidade_nome = df_filtrado['Cidade'].iloc[0]
        
        # Clima
        temp = df_filtrado["Temperatura"].iloc[0]
        sensacao = df_filtrado["Sensação Térmica"].iloc[0]
        umidade = df_filtrado["Umidade"].iloc[0]
        descricao = df_filtrado["Descrição"].iloc[0]
        vento = df_filtrado["Velocidade do Vento"].iloc[0]
        
        # Poluição (Extraindo do dicionário)
        dados_poluicao = df_filtrado["Poluição do Ar"].iloc[0]
        aqi = dados_poluicao['aqi']
        pm2_5 = dados_poluicao['pm2_5']
        pm10 = dados_poluicao['pm10']
        
        # Traduz o AQI para texto
        aqi_texto, aqi_emoji, aqi_cor = traduzir_aqi(aqi)

        # Previsão Bruta
        lista_previsao_raw = df_filtrado["Previsão"].iloc[0]

        # Hora da atualização
        hora = time.strftime("%H:%M", time.localtime())
        
        # --- LAYOUT VISUAL ---
        
        # Cabeçalho da Cidade
        st.subheader(f"📍 {cidade_nome} - Atualizado às {hora}")
        
        # BLOCO 1: Métricas Principais (Dentro de um container com borda)
        with st.container(border=True):
            col1, col2, col3, col4 = st.columns(4)
            
            col1.metric("Temperatura", f"{int(temp)}°C", f"Sensação {int(sensacao)}°C")
            col2.metric("Condição", descricao.title())
            col3.metric("Umidade", f"{umidade}%")
            col4.metric("Vento", f"{vento} m/s")

        # BLOCO 2: Qualidade do Ar (Novo!)
        st.markdown("### 🌱 Qualidade do Ar")
        with st.container(border=True):
            c_ar1, c_ar2, c_ar3 = st.columns([2, 1, 1])
            
            # Mostra o índice AQI com cor
            c_ar1.markdown(f"**Índice AQI:** <span style='color:{aqi_cor}; font-size:20px'>**{aqi} - {aqi_texto} {aqi_emoji}**</span>", unsafe_allow_html=True)
            c_ar1.caption("Escala de 1 (Bom) a 5 (Muito Ruim).")
            
            c_ar2.metric("PM2.5", f"{pm2_5}", help="Partículas finas (inaláveis)")
            c_ar3.metric("PM10", f"{pm10}", help="Partículas inaláveis grossas")

        st.divider()

        # BLOCO 3: Tabela 48h Estilizada
        st.subheader("📅 Previsão: Próximas 48 Horas")
        
        df_48h = f.formatar_previsao_48h(lista_previsao_raw)
        
        # Convertemos temperatura para número puro para usar o ProgressColumn
        # Removemos o "°C" da string para que o gráfico funcione
        df_48h['Temp Num'] = df_48h['Temperatura'].str.replace('°C', '').astype(float)

        st.dataframe(
            df_48h,
            use_container_width=True,
            hide_index=True,
            column_order=("Data/Hora", "Temp Num", "Condição"), # Define a ordem
            column_config={
                "Data/Hora": st.column_config.TextColumn(
                    "Horário",
                    help="Dia e Hora da previsão"
                ),
                "Temp Num": st.column_config.ProgressColumn(
                    "Temperatura (°C)",
                    format="%.1f°C",
                    min_value=0,
                    max_value=45,
                    help="Barra visual da temperatura"
                ),
                "Condição": st.column_config.TextColumn(
                    "Clima",
                )
            }
        )
        
    except Exception as e:
        st.error(f"Ocorreu um erro ao processar os dados: {e}")
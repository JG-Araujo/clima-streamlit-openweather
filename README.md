# 🌤️ Clima Hoje — Técnicas de Programação para Ciência de Dados

Aplicação desenvolvida em Streamlit que permite ao usuário consultar o clima atual, previsão do tempo e qualidade do ar de qualquer cidade, utilizando dados da API OpenWeather.

---
📁 Estrutura do Projeto

--> `app.py`

Arquivo principal da aplicação.

* Configura a página do Streamlit
* Controla o fluxo geral da aplicação
* Integra filtros, tabelas e gráficos
* Organiza o layout visual (métricas, gráficos e tabelas)
* Trata exceções durante a execução

---

--> `filtros.py`

Responsável pela entrada de dados e comunicação com as APIs.

* Carrega e trata o arquivo `city.list.json`
* Renderiza os filtros de país e cidade na sidebar
* Busca dados de clima atual, previsão e poluição do ar
* Formata dados auxiliares para gráficos

---

--> `servicos_api/api_clima.py`

Camada de acesso às APIs do OpenWeather.

* Current Weather API
* 5 Day / 3 Hour Forecast API
* Air Pollution API
* Centraliza as requisições HTTP e tratamento das respostas

---

--> `visualizacoes/graficos.py`

Contém todas as visualizações gráficas da aplicação.

* Gráfico de clima atual
* Gráfico de previsão de temperatura
* Gráfico de qualidade do ar
* Utiliza Plotly para visualizações interativas

---

--> `visualizacoes/tabelas.py`

Responsável pela formatação das tabelas exibidas no app.

* Tabela de clima atual
* Tabela estilizada de previsão das próximas 48h
* Inclui emojis e formatação amigável para o usuário

---

--> `util.py`

Arquivo de funções utilitárias.

* Tradução do índice AQI para texto, emoji e cor
* Funções auxiliares de padronização e validação

---

--> `city.list.json`

Base de dados local com cidades do mundo inteiro.

* Contém nome da cidade, país e coordenadas geográficas
* Usado para geolocalização das consultas à API

---

Projeto Desenvolvido pelos alunos:
- Carlos Abimael Oliveira do Nascimento
- Igor Uchoa Santiago
- João Gabriel dos Santos Araújo

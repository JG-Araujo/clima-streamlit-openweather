# Módulo de Acesso à API OpenWeather

Este módulo é responsável por acessar as APIs do OpenWeather utilizadas no projeto.

## Arquivos
- api_clima.py → Funções de acesso às APIs
- config.py → Arquivo de configuração da API Key

## Funções disponíveis
- obter_coordenadas(cidade)
- obter_clima_atual(latitude, longitude)
- obter_previsao(latitude, longitude)
- obter_poluicao_ar(latitude, longitude)

## Tratamento de erros
O módulo trata os seguintes casos:
- Cidade inexistente ou não encontrada
- Erro de resposta da API OpenWeather
- Problemas de comunicação com a API

## Observações
- Caso a API Key não esteja ativa, será necessário criar uma nova conta no OpenWeather
- A API Key deve ser colocada no arquivo config.py
- Este módulo deve ser importado pelo arquivo principal da aplicação Streamlit.
- A interface em Streamlit deve apenas importar este módulo, receber o nome da cidade e exibir os dados retornados.
- Os nomes de variáveis e funções estão em português para facilitar a leitura
- Já parâmetros da API permanecem em inglês por exigência da especificação do OpenWeather.

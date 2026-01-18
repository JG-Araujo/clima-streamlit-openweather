import requests
import sys
#from config import chave_api
sys.stdout.reconfigure(encoding='utf-8')

chave_api = "6533ed7c4156b67c8bd9f53f295c87a1"

def obter_coordenadas(cidade):
    url = "https://api.openweathermap.org/geo/1.0/direct"
    parametros = {
        "q": cidade,   
        "limit": 1,        
        "appid": chave_api  
    }

    resposta = requests.get(url, params=parametros)

    if resposta.status_code != 200:
        raise Exception("Erro ao acessar a API de geolocalização")

    dados = resposta.json()

    if not dados:
        raise ValueError("Cidade não encontrada")

    return dados[0]["lat"], dados[0]["lon"]


def obter_clima_atual(latitude, longitude):
    url = "https://api.openweathermap.org/data/2.5/weather"
    parametros = {
        "lat": latitude, 
        "lon": longitude, 
        "units": "metric", 
        "lang": "pt_br",    
        "appid": chave_api  
    }

    resposta = requests.get(url, params=parametros)

    if resposta.status_code != 200:
        raise Exception("Erro ao buscar o clima atual")

    dados = resposta.json()

    return {
        "temperatura": dados["main"]["temp"],
        "sensacao": dados["main"]["feels_like"],
        "umidade": dados["main"]["humidity"],
        "descricao": dados["weather"][0]["description"],
        "vento": dados["wind"]["speed"]
    }


def obter_previsao(latitude, longitude):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    parametros = {
        "lat": latitude,  
        "lon": longitude,   
        "units": "metric",  
        "lang": "pt_br",    
        "appid": chave_api  
    }

    resposta = requests.get(url, params=parametros)

    if resposta.status_code != 200:
        raise Exception("Erro ao buscar a previsão do tempo")

    dados = resposta.json()

    previsao = []
    for item in dados["list"]:
        previsao.append({
            "data": item["dt_txt"],              
            "temperatura": item["main"]["temp"],
            "descricao": item["weather"][0]["description"]
        })

    return previsao


def obter_poluicao_ar(latitude, longitude):
    url = "https://api.openweathermap.org/data/2.5/air_pollution"
    parametros = {
        "lat": latitude, 
        "lon": longitude, 
        "appid": chave_api 
    }

    resposta = requests.get(url, params=parametros)

    if resposta.status_code != 200:
        raise Exception("Erro ao buscar dados de poluição do ar")

    dados = resposta.json()
    informacoes = dados["list"][0]

    return {
        "aqi": informacoes["main"]["aqi"],
        "pm2_5": informacoes["components"]["pm2_5"],
        "pm10": informacoes["components"]["pm10"]
    }


if __name__ == "__main__":
    cidade = "Fortaleza"

    latitude, longitude = obter_coordenadas(cidade)
    print("Coordenadas:", latitude, longitude)

   # print("Clima atual:", obter_clima_atual(latitude, longitude))
    print("Previsão:", obter_previsao(latitude, longitude)[:3])
    #print("Poluição do ar:", obter_poluicao_ar(latitude, longitude))
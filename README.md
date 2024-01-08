# weather-api

A presente API obtem a previsão do tempo para os próximos cinco dias, utilizando como parametro uma determinada cidade através do site [OpenWeatherMap] (https://openweathermap.org/). Armazena os dados em uma base de dados não relacional MONGODB para posterio consumo das informações armazenadas.

## Requisitos Necessários 

É necessário que se tenha instalado no ambiente a aplicações Docker e o Docker Compose.

- [Guia Docker](https://docs.docker.com/get-docker/)
- [Guia Docker Compose](https://docs.docker.com/compose/install/)


## Inicializando o projeto

Acesse a pasta raizentech_test e construa o ambiente virtualizado utilizando o docker

```
docker build -t raizentech .
```

Uma vez o consturido(build) o ambiente virtualizado do projeto execute o comando abaixo para subir o container

```
docker run -p 5000:5000 raizentech
```
Após o ambiente ser inicializado acessar a aplicação execute em outro terminal o comando abaixo para obter ID da aplicação

docker ps

```

Acesse o conteiner atráves do comando abaixo:

sudo docker exec -it COLOQUE_ID_AQUI /bin/bash

ID OBTIDO NA ETAPA ACIMA.

```
Após o ambiente ser inicializado acessar a aplicação

curl http://127.0.0.1:5000/weather?city=curitiba


```
Para executar os testes com o framework de teste unittest, você pode seguir estas etapas:

    Certifique-se de que o ambiente virtualizado do Docker está em execução com o seu aplicativo Flask. Se ainda não estiver, você pode iniciá-lo.

    Abra um terminal.

    Navegue até o diretório que contém seus arquivos de teste. Vamos supor que os testes estejam no diretório test_unit.

    Execute o seguinte comando para executar os testes:

python -m unittest test_unit.test_weather_app

```
## Documentação do Código para API de Previsão do Tempo

```
raizentech_test/weather_app.py

Este arquivo é a aplicação principal do Flask, fornecendo um ponto de extremidade da API para recuperar dados meteorológicos.

    Inicialização:
        from flask import Flask, jsonify, request: Importa os módulos necessários do Flask.
        from config.config import weather_app, configure_app: Importa a instância da aplicação Flask e a função de configuração.
        from logging_utils.logging_utils import setup_logging: Importa a função de configuração de log.
        from mongodb_utils.mongodb_utils import connect_to_mongodb, fetch_weather_data, save_to_mongodb: Importa funções relacionadas ao MongoDB.
        weather_app = Flask(__name__): Inicializa a aplicação Flask.

    Configuração e Setup:
        if __name__ == '__main__':: Executa o bloco de código seguinte se o script for executado diretamente.
        configure_app(): Configura a aplicação Flask com as configurações do MongoDB e OpenWeatherMap API.
        setup_logging(): Configura o log para a aplicação.

    Ponto de Extremidade da API:
        @weather_app.route('/weather', methods=['GET']): Define um ponto de extremidade para a rota /weather, acessível por meio de requisições HTTP GET.
        def get_weather():: Define a função para lidar com as requisições à rota /weather.
        city = request.args.get('city', 'São Paulo'): Obtém o parâmetro da cidade da string de consulta com um valor padrão de 'São Paulo'.
        api_key = weather_app.config['OPENWEATHERMAP_API_KEY']: Obtém a chave da API OpenWeatherMap a partir da configuração da aplicação Flask.

    Recuperação de Dados Meteorológicos:
        weather_history_collection = connect_to_mongodb(weather_app): Estabelece uma conexão com o MongoDB e recupera a coleção de histórico meteorológico.
        weather_data = fetch_weather_data(city, api_key): Recupera dados meteorológicos da API OpenWeatherMap.
        save_to_mongodb(weather_history_collection, city, weather_data): Salva os dados meteorológicos recuperados no MongoDB.

    Tratamento de Respostas:
        return jsonify(weather_data): Retorna uma resposta JSON contendo os dados meteorológicos recuperados.
        except requests.exceptions.RequestException as e:: Trata exceções levantadas durante a requisição à API.
        weather_app.logger.error(f"Failed to fetch weather data: {str(e)}"): Registra uma mensagem de erro.
        return jsonify({'error': 'Failed to fetch weather data'}), 500: Retorna uma resposta de erro se a recuperação de dados meteorológicos falhar.

    Executar a Aplicação:
        weather_app.run(debug=True, host='127.0.0.1'): Inicia a aplicação Flask em modo de depuração no localhost.
```
config/config.py

Este arquivo fornece configurações para a aplicação Flask.

    Inicialização:
        from flask import Flask: Importa o módulo Flask.
        import os: Importa o módulo do sistema operacional.
        weather_app = Flask(__name__): Inicializa a instância da aplicação Flask.

    Função de Configuração:
        def configure_app():: Define uma função para configurar a aplicação Flask.
        weather_app.config['MONGO_URI']: Define a URI de conexão com o MongoDB.
        weather_app.config['OPENWEATHERMAP_API_KEY']: Define a chave da API OpenWeatherMap.

```
logging_utils/logging_utils.py

Este arquivo contém funções utilitárias para configurar o log.

    Inicialização:
        import logging: Importa o módulo de log.

    Função de Configuração de Log:
        def setup_logging():: Define uma função para configurar o log.
        logging.basicConfig(filename='weather_app.log', level=logging.DEBUG): Configura o log para um arquivo com nível DEBUG.
```

mongodb_utils/mongodb_utils.py

Este arquivo contém funções utilitárias para operações no MongoDB.

    Inicialização:
        from pymongo import MongoClient: Importa o MongoClient da biblioteca pymongo.
        from datetime import datetime: Importa o módulo de data e hora.
        import requests: Importa o módulo de requisições.
        import logging: Importa o módulo de log.

    Função de Conexão com o Banco de Dados:
        def connect_to_mongodb(app):: Define uma função para conectar ao MongoDB.
        client = MongoClient(app.config['MONGO_URI']): Estabelece uma conexão com o MongoDB usando a URI fornecida.
        weather_history_collection = db['weather_history']: Recupera a coleção 'weather_history'.

    Função de Recuperação de Dados Meteorológicos:
        def fetch_weather_data(city, api_key):: Define uma função para recuperar dados meteorológicos.
        url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}': Constrói a URL para a requisição à API OpenWeatherMap.
        response = requests.get(url): Realiza a requisição à API.
        response.raise_for_status(): Gera um HTTPError para respostas ruins (4xx e 5xx).
        return response.json(): Retorna os dados em formato JSON.

    Função de Salvamento no MongoDB:
        def save_to_mongodb(collection, city, weather_data):: Define uma função para salvar dados no MongoDB.
        history_entry = {'city': city, 'timestamp': datetime.utcnow(), 'weather_data': weather_data}: Cria uma entrada de histórico.
        collection.insert_one(history_entry): Insere a entrada no MongoDB.
```

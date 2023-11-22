# Desafio Técnico - Pessoa Desenvolvedora Fullstack Júnior
## Back End

- Python 3.10.4
- Banco de dados - MongoDB
- Padrão RESTFul
- Para consumir a API necessita autenticação, HTTP Basic 



## Como Instalar e Executar
```bash
# Instalar as bibliotecas python necessárias:
pip install -r requirements.txt

# Configurar variáveis de ambiente:
# String de conexão com o banco de dados MongoDB
export MDB_CONN_STR="mongodb+srv://<user>:<password>@<domain>/?retryWrites=true&w=majority"

# Usuario e senha para consumir a API
export API_USER="admin"
export API_PASSWORD="desafio123"

# Executar a aplicacão:
uvicorn app.main:app --reload
```

# Executando via Docker
```bash
docker build . -f Dockerfile -t desafio-backend

docker run -d --name desafio-backend -p 8000:80 desafio-backend
```

A API estara disponivel no endereço http://localhost:8000
FROM python:3.10-alpine

WORKDIR /src

COPY ./requirements.txt /src/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt

COPY ./app /src/app

ENV MDB_CONN_STR="mongodb+srv://test:kdrsRIjfNrNYYTX5@personcrud.w9kvvra.mongodb.net/?retryWrites=true&w=majority"
ENV API_USER="admin"
ENV API_PASSWORD="desafio123"

CMD ["cd", "src"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

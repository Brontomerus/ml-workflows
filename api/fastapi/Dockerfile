FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./requirements.txt /
COPY ./app /app

RUN pip install -r requirements.txt


WORKDIR /app/

ENV PYTHONPATH=/app

EXPOSE 80


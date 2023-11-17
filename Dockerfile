FROM python:3.11-slim-bookworm

ENV PATH="/scripts:${PATH}"

RUN pip install --upgrade pip


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./scripts /scripts
RUN chmod +x /scripts/*

RUN adduser www-data www-data
USER www-data

COPY ./app ./app
WORKDIR /app


CMD ["entrypoint.sh"]
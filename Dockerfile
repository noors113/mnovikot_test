FROM python:3.10.11

WORKDIR /app
ENV PYTHONUNBUFFERED 1
ENV TZ 'Asia/Bishkek'

RUN pip install -U pip && pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install

# Copy the application code into the container
COPY . .


RUN chmod +x /app/docker-entrypoint.sh

EXPOSE 8000
ENTRYPOINT [ "/app/docker-entrypoint.sh" ]

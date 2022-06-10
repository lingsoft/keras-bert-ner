# Builder
FROM python:3.7-slim as venv
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App
FROM python:3.7-slim
RUN apt-get update && apt-get -y install --no-install-recommends tini && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN addgroup --gid 1001 "elg" && \
    adduser --disabled-password --gecos "ELG User,,," --home /elg --ingroup elg --uid 1001 elg && \
    chmod +x /usr/bin/tini
COPY --chown=elg:elg --from=venv /opt/venv /opt/venv

USER elg:elg
WORKDIR /elg
COPY --chown=elg:elg \
    bert_tokenization.py \
    common.py \
    config.py \
    conlleval.py \
    ner-model/* \
    serve.py \
    tagger.py \
    docker-entrypoint.sh /elg
COPY --chown=elg:elg ./ner-model /elg/ner-model

ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHON_PATH="/opt/venv/bin"
ENV WORKERS=2
ENV TIMEOUT=300
ENV WORKER_CLASS=sync
ENV LOG_LEVEL=info

RUN chmod +x ./docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]

# Imagem Python
# Define um stage comum das imagens de dev e prod chamado base
FROM python:3.10 as base
# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Cria uuário - evitar rodar containers como root em produção
RUN addgroup --system web \
    && adduser --system --ingroup web web
# Instala dependencias de sitema (as root)
RUN apt-get update && apt-get install -y -q --no-install-recommends \
  # dependencias python
  build-essential \
  # dependências postgres (psycopg2)
  libpq-dev \
  # limpa arquivos não usados
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*
# Muda pra usuário web
USER web
# Cria pasta para código
WORKDIR /home/web/code/
# copia lista de dependências do python
COPY --chown=web:web ./requirements/base.txt requirements/base.txt
# Muda temporariamente para o root para evitar problemas com permisões
USER root
# Instala dependênicas do python
RUN pip install --no-cache-dir -r requirements/base.txt
# Copia entrypoint que espera o banco estar disponível
COPY --chown=web:web ./docker/app/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
USER web
# Este código vai rodar antes de cada comando executado no container
ENTRYPOINT ["entrypoint.sh"]


# Define uma imagem para desenvolvimento local. Herda pacotes comuns da base.
FROM base as dev
# Copia o script que inicia o servidor de desenvolvimento (runserver)
COPY --chown=web:web ./docker/app/start-dev-server.sh /usr/local/bin/start-dev-server.sh
USER root
RUN chmod +x /usr/local/bin/start-dev-server.sh
USER web
# O servidor de desenvolvimento inicia com o container
CMD ["start-dev-server.sh"]


# Define uma imagem para produção. Herda pacotes comuns da base.
FROM base as prod
# Instala extras da produção
USER root
COPY --chown=web:web ./requirements/prod.txt requirements/prod.txt
RUN pip install --no-cache-dir -r requirements/prod.txt
# Copia o script que inicia o servidor de desenvolvimento (gunicorn)
COPY --chown=web:web ./docker/app/start-prod-server.sh /usr/local/bin/start-prod-server.sh
RUN chmod +x /usr/local/bin/start-prod-server.sh
USER web
# Copia o código do Django para a pasta que vamos trabalhar
COPY --chown=web:web . ./
# O servidor de produção inicia geralmente junto com o container
CMD ["start-prod-server.sh"]
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

ARG DEPS=requirements

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ Asia/Jakarta
ENV GRPC_PYTHON_DISABLE_DYNAMIC_STUBS 1
ENV PYTHONPATH="$PYTHONPATH:/opt/project/clients/intermediates"
ENV PYTHONPATH="$PYTHONPATH:/opt/project/services/rpc"

COPY . /opt/project
WORKDIR /opt/project

RUN apt-get clean \
    && apt-get update \
    && apt-get install -y tzdata locales-all vim tini gdb \
    && pip install supervisor py-spy pyrasite objgraph \
    && pip install -r ${DEPS}.txt

# Run DB migrations
RUN echo '#! /usr/bin/env sh ' > prestart.sh && \
    echo '# Run migrate firstly... ' >> prestart.sh && \
    echo 'make migrate; ' >> prestart.sh && \
    echo '# Run migrations... ' >> prestart.sh && \
    echo 'make migration; ' >> prestart.sh && \
    echo '# Let the DB ready' >> prestart.sh && \
    echo 'sleep 2; ' >> prestart.sh && \
    echo '# Run migrate secondly...' >> prestart.sh && \
    echo 'make migrate; ' >> prestart.sh

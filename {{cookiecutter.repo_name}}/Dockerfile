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
    && apt-get install -y tzdata locales-all vim tini \
    && pip install supervisor py-spy \
    && pip install -r ${DEPS}.txt

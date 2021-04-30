# ===========
# = Base Image
# ===========

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

# ===========
# = Author
# ===========

LABEL maintainer="bali"

# ===========
# = Initiate Project
# ===========

ENV DEBIAN_FRONTEND=noninteractive

COPY . /opt/project
WORKDIR /opt/project

RUN apt-get clean \
    && apt-get update \
    && apt-get install -y tzdata locales-all vim tini \
    && pip install supervisor py-spy \
    && pip install -r requirements.txt

# Add grpc dir to PYTHONPATH
ENV PYTHONPATH="$PYTHONPATH:/opt/project/clients/intermediates"
ENV PYTHONPATH="$PYTHONPATH:/opt/project/services/rpc"

# Disable grpc dynamic import
ENV GRPC_PYTHON_DISABLE_DYNAMIC_STUBS 1

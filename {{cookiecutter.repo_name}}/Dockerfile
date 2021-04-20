# ===========
# = Base Image
# ===========

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# ===========
# = Author
# ===========

LABEL maintainer="finture"

# ===========
# = Initiate Project
# ===========

ENV DEBIAN_FRONTEND=noninteractive

# Define id_ID.UTF-8
ENV LANGUAGE id_ID.UTF-8
ENV LANG id_ID.UTF-8
ENV LC_ALL id_ID.UTF-8
ENV LC_CTYPE id_ID.UTF-8
ENV LC_MESSAGES id_ID.UTF-8

# Define timezone
ENV TZ Asia/Jakarta

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt \
    && pip install supervisor py-spy \
    && wget https://github.com/apache/rocketmq-client-cpp/releases/download/2.0.0/rocketmq-client-cpp-2.0.0.amd64.deb \
    && dpkg -i rocketmq-client-cpp-2.0.0.amd64.deb

# Add Tini
ENV TINI_VERSION v0.18.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

# Add grpc dir to PYTHONPATH
ENV PYTHONPATH="$PYTHONPATH:/app/clients/intermediates"
ENV PYTHONPATH="$PYTHONPATH:/app/services/rpc"

# Disable grpc dynamic import
ENV GRPC_PYTHON_DISABLE_DYNAMIC_STUBS="1"

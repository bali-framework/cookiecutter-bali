from bali.interceptors import ProcessInterceptor
from loguru import logger

from services.rpc import {{cookiecutter.repo_name}}_pb2 as pb2
from services.rpc import {{cookiecutter.repo_name}}_pb2_grpc as pb2_grpc


class Service(pb2_grpc.{{cookiecutter.repo_name|title}}ServiceServicer):
    pass


if __name__ == '__main__':
    serve()

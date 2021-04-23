from concurrent import futures

import grpc
from bali.interceptors import ProcessInterceptor
from loguru import logger

from services.rpc import {{cookiecutter.repo_name}}_pb2 as pb2, {{cookiecutter.repo_name}}_pb2_grpc as pb2_grpc


class {{cookiecutter.repo_name|title}}Service(pb2_grpc.{{cookiecutter.repo_name|title}}ServiceServicer):
    pass


def serve():
    port = 9080
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors=[ProcessInterceptor()],
    )
    pb2_grpc.add_{{cookiecutter.repo_name|title}}ServiceServicer_to_server({{cookiecutter.repo_name|title}}Service(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logger.info("Service started on port: {}", port)
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

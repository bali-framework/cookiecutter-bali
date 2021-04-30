# loguru log example
```python
from loguru import logger
logger.info("Hello {}", "World")
```
# Make Develop Env
```shell
make env
```
# Make Migration
```shell
alembic revision --autogenerate
```
# Make Migrate
```shell
alembic upgrade head
```
# Start Testing
```shell
tox
```
# If build orjson, ujson dependencies failed
```shell
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
rustup default nightly
```

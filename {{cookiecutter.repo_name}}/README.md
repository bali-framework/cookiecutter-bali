# Loguru usage example
```python
from loguru import logger
logger.info("Hello {}", "World")
```
# Make develop env
```shell
make env
```
# Also, you can develop with docker interpreter
```shell
make docker
```
# Make migration
```shell
make migration
```
# Make migrate
```shell
make migrate
```
# Make testing
```shell
tox
```
# If build orjson, ujson failed
```shell
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
rustup default nightly
```

# Make Develop Env using Python 3.7
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

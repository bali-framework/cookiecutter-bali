# Make Develop Env
```shell
sudo make env
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

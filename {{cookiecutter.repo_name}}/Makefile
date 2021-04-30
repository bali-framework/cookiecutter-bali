env:
	rm -rf venv
	python3 -m venv venv
	. venv/bin/activate \
	&& pip3 install wheel \
	&& pip3 install -r requirements_dev.txt \
	&& pip3 install pre-commit \
	&& pre-commit install

docker:
	docker build --rm --build-arg DEPS=requirements_dev . -t {{cookiecutter.repo_name}}
	pip3 install pre-commit
	pre-commit install

migration:
	alembic revision --autogenerate

migrate:
	alembic upgrade head

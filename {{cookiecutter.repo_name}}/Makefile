env:
	pip3 install wheel pre-commit git+https://github.com/Ed-XCF/bali-cli.git@v0.5.11#egg=bali-cli
	pre-commit install
	rm -rf venv
	python3 -m venv venv
	. venv/bin/activate \
	&& python3 -m pip install --upgrade pip \
	&& pip3 install -r requirements_dev.txt

docker:
	pip3 install wheel pre-commit git+https://github.com/Ed-XCF/bali-cli.git@v0.5.11#egg=bali-cli
	pre-commit install
	docker build --rm --build-arg DEPS=requirements_dev . -t {{cookiecutter.repo_name}}

migration:
	alembic revision --autogenerate

migrate:
	alembic upgrade head

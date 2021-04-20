env:
	rm -rf venv
	python3.8 -m venv venv
	. venv/bin/activate \
	&& pip3 install wheel \
	&& pip3 install -r requirements_dev.txt \
	&& pip3 install pre-commit \
	&& pre-commit install

test:
	coverage run -m pytest -v \
	&& coverage report

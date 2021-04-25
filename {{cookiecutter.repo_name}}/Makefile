env:
	locale-gen id_ID.UTF-8
	rm -rf venv
	python3 -m venv venv
	. venv/bin/activate \
	&& pip3 install wheel \
	&& pip3 install -r requirements_dev.txt \
	&& pip3 install pre-commit \
	&& pre-commit install

tests:
	PYTHONPATH=$(shell pwd) .venv/bin/pytest

run:
	jupyter notebook

create:
	./create_venv.sh

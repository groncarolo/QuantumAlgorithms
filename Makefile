tests:
	PYTHONPATH=$(shell pwd) .venv/bin/pytest

flake:
	flake8_nb b92.ipynb
	flake8_nb bb94.ipynb
	flake8_nb berstein_vazirani.ipynb
	flake8_nb deutsch.ipynb
	flake8_nb deutsch_jozsa.ipynb
	flake8_nb grover.ipynb
	flake8_nb no_cloning_theorem.ipynb
	flake8_nb oracles.ipynb
	flake8_nb qft.ipynb
	flake8_nb shor.ipynb
	flake8_nb simon.ipynb
	flake8_nb teleportation.ipynb
	flake8_nb machine_learning/squared_distance_classifier.ipynb
	flake8 oracle.py
	flake8 test_bb94.py
	flake8 test_deutsch_jozsa.py
	flake8 test_grover.py
	flake8 test_qft.py
	flake8 test_simon.py
	flake8 test_b92.py
	flake8 test_berstein_vazirani.py
	flake8 test_deutsch.py
	flake8 test_oracles.py
	flake8 test_shor.py
	flake8 test_teleportation.py

run:
	jupyter notebook

create:
	./create_venv.sh

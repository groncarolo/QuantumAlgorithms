tests:
	PYTHONPATH=$(shell pwd) .venv/bin/pytest

OPT=--max-line-length 80

flake:
	flake8_nb $(OPT) b92.ipynb
	flake8_nb $(OPT) bb94.ipynb
	flake8_nb $(OPT) berstein_vazirani.ipynb
	flake8_nb $(OPT) deutsch.ipynb
	flake8_nb $(OPT) deutsch_jozsa.ipynb
	flake8_nb $(OPT) grover.ipynb
	flake8_nb $(OPT) no_cloning_theorem.ipynb
	flake8_nb $(OPT) oracles.ipynb
	flake8_nb $(OPT) qft.ipynb
	flake8_nb $(OPT) shor.ipynb
	flake8_nb $(OPT) simon.ipynb
	flake8_nb $(OPT) teleportation.ipynb
	flake8_nb $(OPT) machine_learning/squared_distance_classifier.ipynb
	flake8_nb $(OPT) machine_learning/gates.ipynb
	flake8_nb $(OPT) machine_learning/least_square_estimation.ipynb
	flake8_nb $(OPT) machine_learning/postulate_quantum_mechanics.ipynb
	flake8_nb $(OPT) machine_learning/squared_distance_classifier.ipynb
	flake8_nb $(OPT) machine_learning/states_observables.ipynb
	flake8_nb $(OPT) machine_learning/swap_test.ipynb
	flake8_nb $(OPT) machine_learning/HadamardTest.ipynb
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

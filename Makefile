# Available test targets (run a single suite):
#   make test-b92
#   make test-bb94
#   make test-berstein-vazirani
#   make test-deutsch
#   make test-deutsch-jozsa
#   make test-grover
#   make test-oracles
#   make test-qft
#   make test-shor
#   make test-simon
#   make test-teleportation

PYTEST = PYTHONPATH=$(shell pwd) .venv/bin/pytest
OPT    = --max-line-length 80

# ------------------------------------------------------------------ #
# help -- list all available targets
# ------------------------------------------------------------------ #
.PHONY: help
help:
	@echo ""
	@echo "Available make targets:"
	@echo ""
	@echo "  tests                  Run the full test suite"
	@echo ""
	@echo "  Single-algorithm tests:"
	@echo "    test-b92             B92 QKD protocol"
	@echo "    test-bb94            BB94 QKD protocol"
	@echo "    test-berstein-vazirani  Berstein-Vazirani algorithm"
	@echo "    test-deutsch         Deutsch algorithm"
	@echo "    test-deutsch-jozsa   Deutsch-Jozsa algorithm"
	@echo "    test-grover          Grover search algorithm"
	@echo "    test-oracles         Quantum oracles"
	@echo "    test-qft             Quantum Fourier Transform"
	@echo "    test-shor            Shor factoring algorithm"
	@echo "    test-simon           Simon algorithm"
	@echo "    test-teleportation   Quantum teleportation"
	@echo ""
	@echo "  flake                  Run style checks on all notebooks"
	@echo "  run                    Start Jupyter notebook server"
	@echo "  create                 Create the virtual environment"
	@echo ""

# ------------------------------------------------------------------ #
# tests -- run the full suite
# ------------------------------------------------------------------ #
.PHONY: tests
tests:
	$(PYTEST)

# ------------------------------------------------------------------ #
# individual test targets
# ------------------------------------------------------------------ #
.PHONY: test-b92
test-b92:
	$(PYTEST) test_b92.py

.PHONY: test-bb94
test-bb94:
	$(PYTEST) test_bb94.py

.PHONY: test-berstein-vazirani
test-berstein-vazirani:
	$(PYTEST) test_berstein_vazirani.py

.PHONY: test-deutsch
test-deutsch:
	$(PYTEST) test_deutsch.py

.PHONY: test-deutsch-jozsa
test-deutsch-jozsa:
	$(PYTEST) test_deutsch_jozsa.py

.PHONY: test-grover
test-grover:
	$(PYTEST) test_grover.py

.PHONY: test-oracles
test-oracles:
	$(PYTEST) test_oracles.py

.PHONY: test-qft
test-qft:
	$(PYTEST) test_qft.py

.PHONY: test-shor
test-shor:
	$(PYTEST) test_shor.py

.PHONY: test-simon
test-simon:
	$(PYTEST) test_simon.py

.PHONY: test-teleportation
test-teleportation:
	$(PYTEST) test_teleportation.py

# ------------------------------------------------------------------ #
# flake -- style checks
# ------------------------------------------------------------------ #
.PHONY: flake
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

# ------------------------------------------------------------------ #
# utilities
# ------------------------------------------------------------------ #
.PHONY: run
run:
	jupyter notebook

.PHONY: create
create:
	./create_venv.sh

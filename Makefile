SRC=\
./cloning/no_cloning_theorem.py \
./teleportation/teleportation.py \
./oracles/deutsch_jozsa.py \
./oracles/grover.py \
./oracles/simon.py \
./oracles/oracle.py \
./oracles/shor.py \
./oracles/deutsch.py \
./oracles/berstein_vazirani.py \
./bb84/bb84.py \
./b92/b92.py \
./util/util.py \
./qft/qft.py

all: tests

tests:
	PYTHONPATH=$(shell pwd) .venv/bin/pytest

pylint:
	PYTHONPATH=$(shell pwd); pylint --good-names "a,b,c,d,f,g,i,j,o,p,ph,r,s,s1,s2,t,th,v,x,y,z,N" $(SRC)

flake:
	PYTHONPATH=$(shell pwd); flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	PYTHONPATH=$(shell pwd); flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

run_no_cloning_theorem:
	PYTHONPATH=$(shell pwd) .venv/bin/python ./cloning/no_cloning_theorem.py

run_teleportation:
	PYTHONPATH=$(shell pwd) .venv/bin/python ./teleportation/teleportation.py

run_deutsch_jozsa:
	PYTHONPATH=$(shell pwd) .venv/bin/pytest -s ./oracles/test_deutsch_jozsa.py

run_grover:
	PYTHONPATH=$(shell pwd) .venv/bin/pytest -s ./oracles/test_grover.py

run_simon:
	PYTHONPATH=$(shell pwd) .venv/bin/pytest -s ./oracles/test_simon.py

run_oracle:
	PYTHONPATH=$(shell pwd) .venv/bin/pytest -s ./oracles/test_oracles.py

run_shor:
	PYTHONPATH=$(shell pwd) .venv/bin/pytest -s ./oracles/test_shor.py

run_deutsch:
	PYTHONPATH=$(shell pwd) .venv/bin/pytest -s ./oracles/test_deutsch.py

run_berstein_vazirani:
	PYTHONPATH=$(shell pwd) .venv/bin/pytest -s ./oracles/test_berstein_vazirani.py

run_bb84:
	PYTHONPATH=$(shell pwd) .venv/bin/pytest -s ./bb84/test_bb84.py

run_b92:
	PYTHONPATH=$(shell pwd) .venv/bin/pytest -s ./b92/test_b92.py

run_util:
	PYTHONPATH=$(shell pwd) .venv/bin/pytest -s ./util/test_util.py

run_qft:
	PYTHONPATH=$(shell pwd) .venv/bin/pytest -s ./qft/test_qft.py

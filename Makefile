SRC=\
./cloning/no_cloning_theorem.py \
./teleportation/teleportation.py \
./oracles/deutsch_jozsa.py \
./oracles/util.py \
./oracles/grover.py \
./oracles/simon.py \
./oracles/oracle.py \
./oracles/shor.py \
./oracles/deutsch.py \
./oracles/berstein_vazirani.py \
./bb84/bb84.py \
./b92/b92.py \
./qft/qft.py

all: tests

tests:
	PYTHONPATH=$(shell pwd) .venv/bin/pytest

pylint:
	PYTHONPATH=$(shell pwd); pylint --good-names "a,b,c,d,f,g,i,j,o,p,ph,r,s,s1,s2,t,th,v,x,y,z,N" $(SRC)

flake:
	PYTHONPATH=$(shell pwd); flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	PYTHONPATH=$(shell pwd); flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

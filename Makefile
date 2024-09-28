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
./qft/qft.py

all: tests

tests:
	.venv/bin/pytest

pylint:
	pylint --good-names "a,b,c,d,f,g,i,j,o,p,ph,r,s,s1,s2,t,th,v,x,y,z,N" $(SRC)

flake:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

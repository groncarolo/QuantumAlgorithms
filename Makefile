SRC=\
./bb84/bb84.py \
./bb84/tests.py \
./cloning/no_cloning_theorem.py \
./oracles/deutch-jozsa.py \
./oracles/deutch.py \
./oracles/oracle.py \
./oracles/tests.py \
./teleportation/teleportation.py \
./teleportation/tests.py

all: tests

tests:
	.venv/bin/pytest

pylint:
	pylint --good-names "a,b,c,d,f,g,i,j,o,p,ph,r,s,s1,s2,t,th,v,x,y,z" $(SRC)

flake:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

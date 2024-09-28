# Quantum Algorithms

This repository contains a small collection of Quantum Algorithms
developed using Sympy

The algorithms are
- BB84
- No Cloning Theorem
- Quantum Teleportation
- Deutsch's Constant vs Balanced function algorithm
- Deutsch jozsa's generalization algorithm
- Grover's search algorithm
- Shor's factorization algorithm
- Simon's Periodicity algorithm


## Quantum Teleportaion
```
The problem:
Teleport a quantum state

The Solution:
           SENDING      |  RECEIVING
          ------X-------|--X-Z
|PHI+>    ---H--o---X---|--o-|
a|0>+b|1> ----------o-H-|----o
```

## Deutsch
```
The problem:
Given a function f {0, 1} -> {0, 1} that we can evaluate
but is unknown to us determine if it is balanced or
constant
The oracle takes as input Qubits |x> and|y>
and returns |x, y XOR f(x)>

The Solution:
                 +-----------------+
  |x>  |0>---H---|                 |---H--M |x>
                 |       U_f       |
  |y>  |1>---H---|                 |------   |y XOR f(x)>
                 +-----------------+
Constant zero -> +|0>*|->
Constant  one -> -|0>*|->
Balanced 0->1 -> +|1>*|->
Balanced 1->0 -> -|1>*|->
```

## Deutsch jozsa
```
The problem:
This is a generalization of Deutsch algorithm
consider f {0,1}^n  -> f {0, 1}^n that is not known
determine if f is balanced or constant
where f is
balanced if exactly half of the input go to zero ( and the other half to one)
constant if all input go to zero OR all got to one

The Solution:
                     +-----------------+
  |x>  |0>-/n--H*n---|                 |--/n--H*n---M |x>
                     |       U_f       |
  |y>  |1>---H-------|                 |------------  |y XOR f(x)>
                     +-----------------+

Constant zero -> +|0*n>*|->
Constant  one -> -|0*n>*|->
Balanced 0->1 ->  NOT (+|0*n>*|->) and NOT (-|0*n>*|->)
```

## Berstein Vazirani
```
The problem:
We have a function f {0,1}^n -> {0,1}
f(x) = s dot x
s is a n-bit string
s dot x = s_n-1x_n-1 + ... + s1x1 + s0x0
We want to find s = s_n-1...s1s0

The Solution:
                     +-----------------+
  |x>  |0>-/n--H*n---|                 |--/n--H*n---M |x>
                     |       U_f       |
  |y>  |1>---H-------|                 |------------  |y XOR f(x)>
                     +-----------------+
```

## Grover
```
The problem:
Given a function f {0, 1}^n -> {0, 1} that we can evaluate
The oracle takes as input Qubits |x> and|y>
and returns |x, y XOR f(x)>

The Solution:
                    +--------------------------------------------------------+
                    |   sqrt(2**n) times                                     |
                    |            +-----------------+         +---------+     |
  |x>  |0>-/n--H*n--|------------|                 |---\n----| -I - 2A |--\n-|----M
                    |            |       U_f       |         +---------+     |
  |y>               |  |1>---H---|                 |------- |y XOR f(x)>     |
                    |            +-----------------+                         |
                    +--------------------------------------------------------+
We obtain a high probability on the input chosen by f
```

## Shor
```
The problem:
Factor an interger N into its prime factors

The Solution:
                     +-----------------+
  |x>  |0>-/m-H*m----|                 |--/m--QFT+---M |x>
                     |       U_f_a,N   |
  |y>  |0>-/n--------|                 |--/n--------  |y XOR f(x, a, N)>
                     +-----------------+
```

## Simon
```
The problem:
consider f {0,1}^n  -> f {0, 1}^n that is not known
we are told that exists c = c0c1c2...cn-1
such that for all string x, y belonging to {0,1}^n
we have
f(x) == f(y)  if and only if x = y XOR c

The Solution:
                     +-----------------+
  |x>  |0>-/n--H*n---|                 |--/n--H*n---M |x>
                     |       U_f       |
  |y>  |0>-/n--------|                 |--/n--------  |y XOR f(x)>
                     +-----------------+
```

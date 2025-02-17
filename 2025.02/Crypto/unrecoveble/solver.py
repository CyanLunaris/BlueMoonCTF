# Z3 - install from pip, even on Windows it works out-of-box
# STP (https://github.com/stp/stp) Instruction:
# 1. Install using instruction from repo
# 2. Apply fix: https://github.com/stp/stp/issues/454
# 3. run like "LD_LIBRARY_PATH=/home/kali/stp/deps/minisat/build:/home/kali/stp/deps/install/lib:/home/kali/stp/deps/cadiback:/home/kali/stp/deps/cadical/build python3 solver.py"

import random
# import stp
import z3

RNG_SEED = 0x4C55464659
DENSITY_FACTOR = 8

def reseed_rng():
    random.seed(a=RNG_SEED, version=2)


def iteration_for_solver(solver, src, dest):  # add constraints to solver that Transform(src) == dest
    src_len = len(src)
    density = src_len * DENSITY_FACTOR
    for i in range(density):
        a, b = random.randint(0, src_len - 1), random.randint(0, src_len - 1)
        op_type = random.randint(0, 2)
        if op_type == 0:
            solver.add(dest[i] == (src[a] ^ src[b]))
        elif op_type == 1:
            solver.add(dest[i] == (src[a] + src[b]))
        elif op_type == 2:
            solver.add(dest[i] == (src[a] & src[b]))
        else:
            print('panic! (unknown op_type)')
            exit(1)
    return src


def n_iters_for_solver(flag_len, dest, N, solver_type=z3.Solver):
    reseed_rng()
    solver = solver_type()

    if solver_type == z3.Solver:
        solver_bitvec = z3.BitVec
    else:  # stp
        solver_bitvec = solver.bitvec

    FLAG = [solver_bitvec(f's{i}', 8) for i in range(flag_len)]
    for sym in FLAG:
        solver.add(sym >= 32)
        solver.add(sym <= 127)
    virtual_symbols = [[solver_bitvec(f'v{layer}s{i}', 8) for i in range(flag_len * (DENSITY_FACTOR ** layer))] for
                       layer in range(1, N)]
    if N == 1:  # connect directly
        iteration_for_solver(solver, FLAG, dest)
    else:  # connect through inner layers
        iteration_for_solver(solver, FLAG, virtual_symbols[0])

        k = 0
        for i in range(N - 2):
            print(f'connecting inner layer #{i}')
            iteration_for_solver(solver, virtual_symbols[i], virtual_symbols[i + 1])
            k = i

        iteration_for_solver(solver, virtual_symbols[k + 1], dest)

    if solver_type == z3.Solver:
        if solver.check() == z3.sat:
            return [solver.model()[f].as_long() for f in FLAG]
        else:
            print("No solution found")
            exit(1)
    else:  # stp
        print(solver.check())
        mdl = solver.model()
        res = []
        for v in mdl:
            if v.startswith('s'):
                res.append(mdl[v])
        return res


layers = 5
with open('flag.enc', 'rb') as f:
    encrypted = f.read()

len_flag = len(encrypted)

for _ in range(layers):
    len_flag //= DENSITY_FACTOR
print('Length of the flag:', len_flag)
# flag_recovered = ''.join([chr(x) for x in n_iters_for_solver(len_flag, encrypted, layers, solver_type=stp.Solver)])
flag_recovered = ''.join([chr(x) for x in n_iters_for_solver(len_flag, encrypted, layers, solver_type=z3.Solver)])
print(flag_recovered)

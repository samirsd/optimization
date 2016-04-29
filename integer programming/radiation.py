#!/usr/bin/python

# http://stackoverflow.com/questions/36518205/two-dimensional-bin-packing

# http://www.dcc.fc.up.pt/~jpp/seminars/azores/gurobi-intro.pdf




from gurobipy import *

import math

# problem data
m, n = 2, 3

I = [
    [2, 4, 3],
    [3, 4, 2]]

# m, n = 5, 5
# I = [[0, 3, 3, 0, 2],
#      [0, 0, 5, 5, 6],
#      [0, 3, 3, 3, 5],
#      [0, 4, 4, 6, 5],
#      [0, 3, 3, 2, 3]]

# print(I[1][1], "I 2,2")

mdl = Model("delivery opt")

Q, S, N = {}, {}, {}


# todo fix

# B_star = m*n
def decompMtx(m, n, I):
    # ~~~~~~ variables ~~~~~~~ #
    # beam on times

    bot = 10
    for b in range(bot):
        for i in range(m):
            for j in range(n):
                Q[b, i, j] = mdl.addVar(vtype=GRB.INTEGER, name="Q[%s,%s,%s]" % (b, i, j))

    for b in range(bot):
        for i in range(m):
            for j in range(n):
                S[b, i, j] = mdl.addVar(lb=0, vtype=GRB.INTEGER, name="S[%s,%s,%s]" % (b, i, j))

    # for i in range(m):
    #     for j in range(n):
    #         I[i, j] = mdl.addVar(lb=0, vtype=GRB.INTEGER, name="I[%s,%s]" % (i, j))

    # K = mdl.addVar(vtype=GRB.INTEGER, name="K")

    # B_star = mdl.addVar(vtype=GRB.INTEGER, name="B_star")

    for b in range(bot):
        N[b] = mdl.addVar(vtype=GRB.INTEGER, name="N")

    mdl.update()

    # ~~~~~~ constraints ~~~~~~~ #


    Q_constr = LinExpr()
    for b in range(1, bot):
        Q_constr += b * Q[b, i, j]


        # for i in range(m):
        #     for j in range(n):
        #         Q_constr = LinExpr()
        #         for z in range( bot):
        #             Q_constr += z+1 * Q[z, i, j]
        #         print(Q_constr)
        #         mdl.addConstr(I[i][j] == Q_constr, name="Q[%s,%s,%s]" % (b, i, j))

    for i in range(m):
        for j in range(n):
            mdl.addConstr(
                I[i][j] == Q[0, i, j] + 2 * Q[1, i, j] + 3 * Q[2, i, j] + 4 * Q[3, i, j] + 5 * Q[4, i, j] + 6 * Q[5, i, j] + 7 * Q[
                    6, i, j] + 8 * Q[7, i, j] + 9 * Q[8, i, j] + 10 * Q[9, i, j])
    for b in range(bot):
        for i in range(m):
            for j in range(n):
                if j - 1 > 0:
                    mdl.addConstr(S[b, i, j], ">=", Q[b, i, j] - Q[b, i, j - 1])
                    # mdl.addConstr(S[b, i, j], ">=", 0)

    # mdl.addConstr()
    for b in range(bot):
        mdl.addConstr(N[b], ">=", quicksum(S[b, i, j] for i in range(m)))

    # mdl.addConstr(K, "=", quicksum(N[b] for b in range(bot)))

    # mdl.addConstr(B_star, "=", quicksum(b * N[b] for b in range(bot)))

    # for b,i,j in range(bot,m,n):

    for b in range(bot):
        for i in range(m):
            for j in range(n):
                mdl.addConstr(Q[b, i, j], "<=", math.floor(I[i][j] / (b + 1)))

    sum = LinExpr()
    for b in range(1, bot):
        sum += b * N[b]
        print(sum)

    mdl.setObjective(sum, GRB.MINIMIZE)
    # mdl.setObjective(quicksum(b * N[b] for b in range(bot)), GRB.MINIMIZE)

    # mdl.setObjective(quicksum(N[b] for b in range(bot)) , GRB.MINIMIZE)

    # B_star * (m * n + 1) (offline)
    # mdl.addConstr(K <= (m * n + 1))

    # mdl.addConstr(Q[(b,i,j)] <= math.floor(I[(i,j)]/b))

    mdl.update()
    mdl.optimize()


decompMtx(m, n, I)

from gurobipy import *
import math
import copy


def createModel(node):
    # Create a new model
    model = Model(node.child['bound'])
    x1_ub = node.model.getVarByName("x1").ub
    x1_lb = node.model.getVarByName("x1").lb
    x2_ub = node.model.getVarByName("x2").ub
    x2_lb = node.model.getVarByName("x2").lb
    # for v in node.variables:

    # make this generic later...
    x1 = model.addVar(lb=x1_lb, ub=x1_ub, vtype=GRB.CONTINUOUS, name='x1')
    x2 = model.addVar(lb=x2_lb, ub=x2_ub, vtype=GRB.CONTINUOUS, name='x2')
    model.update()
    model.setObjective(3 * x1 + 2 * x2, GRB.MAXIMIZE)
    # Add constraint: x + 2 y + 3 z <= 4
    model.addConstr(4 * x1 + 2 * x2 <= 15, "c0")
    # Add constraint: x + y >= 1
    model.addConstr(x1 + 2 * x2 <= 8, "c1")
    model.addConstr(x1 + x2 <= 5, "c2")
    node.model = model
    model.update()

    return node


def init(model):
    variables = []

    for v in model.getVars():
        variables.append(v)
    print variables, "variables"
    objective = model.objVal
    chosenVar = chooseVar(variables)
    child = None
    node = Node(model, variables, objective, chosenVar, child)
    # def __init__(self, model, variables, objective, best, chosenVar, child)

    return node


def chooseVar(variables):
    # if all are integers... return the first solution
    l = []
    print(variables, "variables")

    for v in variables:
        l.append(v.x)

    if all(isinstance(v, int) for v in variables):
        # name = "x1"
        return v
    else:
        for v in variables:
            if not v.x.is_integer():
                return v
                # break


def feasible(node):
    if node.model.status == GRB.INFEASIBLE:
        return False
    return True


def solution(node):
    if all(isinstance(v, int) for v in node.variables) and isinstance(node.objective, int):
        print "solution"
        return True
    print "not a solution"
    return False

def isLeaf():
    return True
def optimal(node):
    if solution(node) and feasible(node) and node.objective >= node.best_value:
        print("OPTIMAL SOLUTION")
        return True
    return False

def evaluate(node):
    # soln = []
    l = []
    if feasible(node):
        node.model.optimize()
        for v in node.model.getVars():
            print('%s %g' % (v.varName, v.x))
            l.append(v.x)
        node.objective = node.model.objVal
        node.variables = l
        if node.objective > node.best_value:
            node.best_value = node.objective
        return node
    else:
        return "infeasible"

def generateLeaf(node):
    node = createModel(node)
    chosenVar = node.chosenVar
    bound = node.child['bound']
    limit = node.child['limit']

    # print(chosenVar, bound)
    if (bound == "ub"):
        node.model.getVarByName(chosenVar.varName).ub = limit
    if (bound == "lb"):
        node.model.getVarByName(chosenVar.varName).lb = limit

    node.model.update()
    # print("new lb", model.getVarByName(chosenVar).lb)
    # print("new ub", model.getVarByName(chosenVar).ub)

    return node


class Node():
    best_value = 0

    def __init__(self, model, variables, objective, chosenVar, child):
        self.model = model
        self.variables = variables
        # z value
        self.objective = objective
        # current optimum (12.5 for test case lp relaxation)
        self.chosenVar = chosenVar
        self.child = child

    def printNode(self):
        node = {}
        node["variables"] = self.variables
        node["objective"] = self.objective
        # node["best"] = self.best
        node['chosenVar'] = self.chosenVar
        node['child'] = self.child
        node['model ub'] = self.model.getVarByName(self.chosenVar.varName).ub
        node['model lb'] = self.model.getVarByName(self.chosenVar.varName).lb
        print(node)

    # left child is upper bound of chosen var
    def getLeftChild(self):
        self.child = {'bound': "ub", 'limit': math.floor(self.chosenVar.x)}
        # self.leftLeaf = updateModel(self.leftLeaf, self.child, self.chosenVar, "ub")
        leftLeaf = generateLeaf(Node(self.model, self.variables, self.objective, self.chosenVar, self.child))
        return leftLeaf

    # in this case computing the ceiling
    def getRightChild(self):
        print self.chosenVar, "chosenvar"
        print self.chosenVar.varName, "name"
        self.child = {'bound': "lb", 'limit': math.ceil(self.chosenVar.x)}
        # self.rightLeaf = updateModel(self.rightLeaf, self.child, self.chosenVar, "lb")
        rightLeaf = generateLeaf(Node(self.model, self.variables, self.objective, self.chosenVar, self.child))
        return rightLeaf


def bb(node):
    node.best_value = 0
    root = evaluate(node)
    stack = [root.getRightChild(), root.getLeftChild()]

    # choose var to branch on x1 or x2 in this case
    # print stack

    # for s in stack: print(s.model.getVarByName(s.chosenVar).ub,s.child)

    while stack:

        count = 0
        count+=1
        print count, "count"
        # best first..
        # node = min(stack, key=lambda i: i.child)

        # depth first
        node = stack[0]
        stack.remove(node)
        print "node initial"
        node.printNode()
        node = evaluate(node)
        if node == "infeasible":
            continue

        if optimal(node):
            return node
        else:
            continue
        #
        # # print(optimal(node))
        #
        # count += 1
        # print "count", count
        # break


m = Model("lp")
# Create variables
x1 = m.addVar(lb=0, ub=1000000, vtype=GRB.CONTINUOUS, name="x1")
x2 = m.addVar(lb=0, ub=1000000, vtype=GRB.CONTINUOUS, name="x2")
# Integrate new variables
m.update()

# print(x1.lb)
m.setObjective(3 * x1 + 2 * x2, GRB.MAXIMIZE)
# Add constraint: x + 2 y + 3 z <= 4
m.addConstr(4 * x1 + 2 * x2 <= 15, "c0")
# Add constraint: x + y >= 1
m.addConstr(x1 + 2 * x2 <= 8, "c1")

m.addConstr(x1 + x2 <= 5, "c2")
m.optimize()

root = init(m)
bb(root)

# a = evaluate(m)

# print(chooseVar(a), "choosefvar")
# b = chooseVar(a)

# updateModel(b,3)
# print(x2.ub,"aksjhdakjsdhskaj")


# if x1 and x2 are both integers then stop and return candidate solution
# if x1 and x2 are both fractional then choose x1
# if only one of the vars is fractional then choose the fractional var

# check if it is a candidate solution or not and whether or not it is feasible
# takes an integer program as input




#     if model.status == GRB.Status.INF_OR_UNBD:
#         # Turn presolve off to determine whether model is infeasible
#         # or unbounded
#         model.setParam(GRB.Param.Presolve, 0)
#         model.optimize()
#     if model.status == GRB.Status.OPTIMAL:
#         print('Optimal objective: %g' % model.objVal)
#         model.write('model.sol')
#         # exit(0)
#     elif model.status != GRB.Status.INFEASIBLE:
#         print('Optimization was stopped with status %d' % model.status)
#         exit(0)
# # return model
#     return model




# self.leftLeaf = createModel(self)
# self.rightLeaf = createModel(self)

# def chooseVar(self):
#     if all(isinstance(item, int) for item in self.variables):
#     # name = "x1"
#         return self.variables.x1
#     else:
#         for v in self.variables:
#             if not (self.variables[v]).is_integer():
#                 return v


# stack[0].printNode()


# node.printNode()
# for s in stack:
#     s.printNode()
# node = updateModel(node)
# node.printNode()
# node.model =

# node = createModel(node)

# # node.model = p
# node = updateModel(node)

# print p, "p"

# # print node.model , "node"

# if p is node.model:
#     print "yes"
# else:
#     print "no"

# node.printNode()


# node.printNode()
# d =  evaluate(node.model)



# if node.best <
# node.printNode()


# returns left or right branch based on branching heuristic
# current heuristic is that if both are fractions, choose first var,
# else choose the fractional var
# Node = branch(stack)

#     # pop the node off the stack to be evaluated
#     stack.remove(node)

#     if node.isInfeasible():
#         continue
#     if node.isCandidate() and node.value > Node.best_value:
#         Node.best_value = node.value
#         Node.best_ip = node.ip
#         continue
#     else:
#         stack.append(node.getLeftChild())
#         stack.append(node.getRightChild())

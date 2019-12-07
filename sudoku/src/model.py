from pyomo.environ import *


data = DataPortal()
data.load(filename='data/model_data.dat')
data.load(filename='data/formatted_data_input.csv', param='A')

model = AbstractModel()

# Index to iterate over variables
model.i = Set()
model.j = Set()
model.k = Set()
model.r = Set()
model.s = Set()

# Aux params:
# A: 1 if i,j,k has a value, 0 otherwise
# xBI: bounds for sum(i) on squares
# xBJ: bounds for sum(i) on squares
model.A = Param(model.i, model.j, within=NonNegativeIntegers, initialize=data['A'], default=0)

# Variables
model.x = Var(model.i, model.j, domain=NonNegativeIntegers)
model.delta = Var(model.i, model.j, model.k, domain=Boolean)


# Constraint: Only one value of each K for each column
def col_constraints(model, j, k):
    return sum(model.delta[i, j, k] for i in model.i) == 1


# Constraint: Only one value of each K for each row
def row_constraints(model, i, k):
    return sum(model.delta[i, j, k] for j in model.j) == 1


# Constraint: Only one value of each K for each box
def value_constraints(model, i, j):
    return sum(model.delta[i, j, k] for k in model.k) == 1


# Constraint: Only one value of each K for each square
def square_constraints(model, r, s, k):
    i_range = range(3 * r - 2, 3 * r + 1)
    j_range = range(3 * s - 2, 3 * s + 1)
    return sum(sum(model.delta[i, j, k] for j in j_range) for i in i_range) == 1


# Low bound
def bound_constraints(model, i, j):
    if model.A[i, j] != 0:
        return model.x[i, j] == model.A[i, j]
    return inequality(1, model.x[i, j], 9)


def delta_x_constraints(model, i, j):
    return model.x[i, j] == sum(k * model.delta[i, j, k] for k in model.k)


def objective_function(model):
    return summation(model.x)


# Generating constraints into the model
model.col_constraints = Constraint(model.j, model.k, rule=col_constraints)
model.row_constraints = Constraint(model.i, model.k, rule=row_constraints)
model.square_constraints = Constraint(model.r, model.s, model.k, rule=square_constraints)
model.x_constraints = Constraint(model.i, model.j, rule=bound_constraints)
model.delta_x_constraints = Constraint(model.i, model.j, rule=delta_x_constraints)
model.value_constraints = Constraint(model.i, model.j, rule=value_constraints)


# Objective Function
model.OBJ = Objective(rule=objective_function, sense=maximize)

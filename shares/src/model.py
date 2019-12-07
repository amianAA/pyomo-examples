from pyomo.environ import *


model = ConcreteModel()

"""
Variables
"""
model.x = Var(['A', 'B', 'T'], domain=NonNegativeReals)


"""
Constraints and Objective Function
"""
# Objective Function
model.OBJ = Objective(expr=0.1*model.x['A'] + 0.08*model.x['B'] + 0.03*model.x['T'], sense=maximize)

# Constraints
model.Constraint1 = Constraint(expr=model.x['A'] + model.x['B'] <= 16000)
model.Constraint2 = Constraint(expr=model.x['T'] >= 2000)
model.Constraint3 = Constraint(expr=model.x['A'] <= 2 * model.x['B'])
model.Constraint4 = Constraint(expr=model.x['A'] + model.x['B'] + model.x['T'] <= 20000)

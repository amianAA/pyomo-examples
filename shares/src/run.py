from pyomo.opt import SolverFactory

import model as shares

instance = shares.model
solver = 'cbc'


def optimise():
    opt = SolverFactory(solver)
    results = opt.solve(instance)
    response = results.json_repn()
    if response['Solver'][0]['Status'] == 'ok':
        time_spent = response['Solver'][0]['System time']
        output = 'Your best investment is the following:'
        for k, v in getattr(instance.x, '_data').items():
            output += f'\n    On option {k}, {round(v.value, 2)} euros'
        print(f'Solution:\n{output} \n\n Time spent: {time_spent} s')
    else:
        print(f'{response["Solver"][0]["Termination message"]}. Please, review input data')


optimise()

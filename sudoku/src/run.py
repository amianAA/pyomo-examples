from pyomo.opt import SolverFactory

import model as sudoku

instance = sudoku.model.create_instance(sudoku.data)
solver = 'cbc'


def optimise():
    opt = SolverFactory(solver)
    results = opt.solve(instance)
    response = results.json_repn()
    if response['Solver'][0]['Status'] == 'ok':
        time_spent = response['Solver'][0]['System time']
        output = ''
        for (i, j), v in getattr(instance.x, '_data').items():
            if i in (1, 4, 7) and j == 1:
                output += '-------------\n'
            if j in (1, 4, 7):
                output += '|'
            output += f'{int(v.value)}'
            if j == 9:
                output += '|\n'
        output += '-------------'
        print(f'Solution:\n {output} \n\n Time spent: {time_spent} s')
    else:
        print(response['Solver'][0]['Termination message'])


optimise()

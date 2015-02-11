import numpy as np
from ortools.linear_solver import pywraplp


def linprog_solve(f, A, b):
    '''
    Solve the following linear programming problem
            minimize_x (f.T).dot(x)
            subject to A.dot(x) <= b
    where   A is sparse matrix
            f is vector of cost function associated with variable
            b is constraints
    '''

    # flatten the variable
    f = f.flatten()
    b = b.flatten()

    solver = pywraplp.Solver('SolveReviewerAssignment',
                     pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

    infinity = solver.Infinity()
    n, m = A.shape
    x = [[]]*m
    c = [0]*n

    for j in range(m):
        x[j] = solver.NumVar(-infinity, infinity, 'x_%u' % j)

    # state objective function
    objective = solver.Objective()
    for j in range(m):
        objective.SetCoefficient(x[j], f[j])
    objective.SetMaximization()

    # state the constraints
    for i in range(n):
        c[i] = solver.Constraint(-infinity, b[i])
        for j in A.col[A.row == i]:
            c[i].SetCoefficient(x[j], A.data[np.logical_and(A.row == i, A.col == j)][0])

    result_status = solver.Solve()
    if result_status != 0:
        "The final solution might not converged"

    x_sol = [x_tmp.SolutionValue() for x_tmp in x]

    return x_sol

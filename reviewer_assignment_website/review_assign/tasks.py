from jobtastic import JobtasticTask
import paper_reviewer_matcher as prm
from scipy.sparse import coo_matrix
try:
    from ortools.linear_solver import pywraplp
except ImportError:
    print "or-tools does not seem to be installed. Skipping for now"

import numpy as np
import pandas as pd
from unidecode import unidecode


class LinearProgrammingAssignment(JobtasticTask):

    significant_kwargs = [
        ('reviewer_abstracts', str),
        ('article_data', str),
        ('people_data', str),
        ('min_rev_art', str),
        ('max_rev_art', str),
        ('min_art_rev', str),
        ('max_art_rev', str),
    ]

    # How long should we give a task before assuming it has failed?
    herd_avoidance_timeout = 5*60  # Shouldn't take more than 5*60 seconds
    # How long we want to cache results with identical ``significant_kwargs``
    cache_duration = -1  # No cache
    # Note: 0 means different things in different cache backends. RTFM for yours.

    def calculate_result(self, reviewer_abstracts, article_data, people_data,
                         min_rev_art, max_rev_art, min_art_rev, max_art_rev):
        """
        Generates a csv file with the resulting assignment while it updates the status
        of the process using Celery
        """

        cur_progress = 0
        max_progress = 100

        article_data = pd.DataFrame(article_data)
        people_data = pd.DataFrame(people_data)

        update_frequency = 1
        cur_progress += int(max_progress/6.)
        self.update_progress(
                cur_progress,
                max_progress,
                update_frequency=update_frequency,
            )


        # this performs the topic modeling (LSA)
        # a = prm.compute_affinity(reviewer_abstracts[0:10], article_data.Abstract.iloc[0:10])
        a = prm.compute_affinity(reviewer_abstracts, article_data.Abstract)
        cur_progress += int(max_progress/6.)
        self.update_progress(
                cur_progress,
                max_progress,
                update_frequency=update_frequency,
            )

        v, A, d = prm.create_lp_matrices(a, min_rev_art, max_rev_art,
                                          min_art_rev, max_art_rev)
        v = v.flatten()
        d = d.flatten()

        cur_progress += int(max_progress/6.)
        self.update_progress(
                cur_progress,
                max_progress,
                update_frequency=update_frequency,
            )

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
            objective.SetCoefficient(x[j], v[j])
        objective.SetMaximization()

        # state the constraints
        for i in range(n):
            c[i] = solver.Constraint(-infinity, d[i])

            # update status bar
            if np.mod(i, int(n/10)) == 0:
                cur_progress += 3
                self.update_progress(
                    cur_progress,
                    max_progress,
                    update_frequency=update_frequency,
                )

            for j in A.col[A.row == i]:
                c[i].SetCoefficient(x[j], A.data[np.logical_and(A.row == i, A.col == j)][0])

        result_status = solver.Solve()
        if result_status != 0:
            print "The final solution might not converged"

        x_sol = np.array([x_tmp.SolutionValue() for x_tmp in x])

        #x = prm.linprog_solve(v, ne, d)
        x_sol = (x_sol > 0.5)

        cur_progress += int(max_progress/6.)
        self.update_progress(
                4*int(max_progress/6.),
                max_progress,
                update_frequency=update_frequency,
            )

        b = prm.create_assignment(x_sol, a)
        self.update_progress(
                5*int(max_progress/6.),
                max_progress,
                update_frequency=update_frequency,
            )

        assignment_df = article_data[['PaperID', 'Title']]
        assignment_df['Reviewers'] = ''
        assignment_df['ReviewerIDs'] = ''
        for i in range(b.shape[0]):
            paper_reviewers = np.where(b[i, :])[0]
            assignment_df.Reviewers.iloc[i] = ', '.join(list(people_data.FullName.iloc[paper_reviewers].copy()))
            # assignment_df.ReviewerIDs.iloc[i] = ', '.join(list(people_data.PersonID.iloc[paper_reviewers].copy()))
        self.update_progress(
                6*int(max_progress/6.),
                max_progress,
                update_frequency=update_frequency,
        )

        # transform to ascii
        assignment_df.Title.apply(lambda x: unicode(x))
        assignment_df.Reviewers.apply(lambda x: unicode(x))

        # , 'result': assignment_df.to_csv(None, na_rep='', index=False)
        # return {'task': {'status': 'SUCCESS'}}
        return assignment_df.to_csv(None, na_rep='', index=False, encoding='utf-8')

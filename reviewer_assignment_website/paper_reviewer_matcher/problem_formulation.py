"""Create linear programming formulation of reviewer assignment problem"""


__all__ = ['create_lp_matrices', 'create_assignment']

import scipy.sparse as sparse
import numpy as np


def create_lp_matrices(a, min_reviewers_per_paper, max_reviewers_per_paper,
                       min_papers_per_reviewer, max_papers_per_reviewer):
    """This function creates the matrices suitable for running Camillo J. Taylor algorithm
        a: affinity matrix
    """
    npapers = a.shape[0]
    nreviewers = a.shape[1]
    nedges = len(a.nonzero()[0])

    i, j = a.nonzero()
    v = a[i, j]

    # reviewers per paper and papers per reviewer
    ne = sparse.dok_matrix((npapers+nreviewers, nedges), dtype=np.float)
    ne[i, range(nedges)] = 1
    ne[j+npapers, range(nedges)] = 1
    d = np.zeros((1, npapers + nreviewers))
    d[0, 0:npapers] = max_reviewers_per_paper
    d[0, npapers:] = max_papers_per_reviewer

    # at least reviewers_per_paper
    ne_atleast1_rev_per_paper = sparse.dok_matrix((npapers, nedges), dtype=np.int)
    ne_atleast1_rev_per_paper[i, range(nedges)] = -1
    d_atleast1_rev_per_paper = -np.ones((1, npapers))*min_reviewers_per_paper

    # at least papers_per_reviewer
    ne_atleast1_paper_per_rev = sparse.dok_matrix((nreviewers, nedges), dtype=np.int)
    ne_atleast1_paper_per_rev[j, range(nedges)] = -1
    d_atleast1_paper_per_rev = -np.ones((1, nreviewers))*min_papers_per_reviewer

    # append the other constrants where x >= 0 and x <= 1
    # x <= 1
    ne0 = sparse.dok_matrix((nedges, nedges), dtype=np.int)
    ne0[range(nedges), range(nedges)] = 1
    d0 = np.ones((nedges, 1))

    # -x <= 0 => x >= 0
    ne1 = sparse.dok_matrix((nedges, nedges), dtype=np.int)
    ne1[range(nedges), range(nedges)] = -1
    d1 = np.zeros((nedges, 1))

    final_ne = sparse.vstack([ne,
                              ne_atleast1_rev_per_paper,
                              ne_atleast1_paper_per_rev,
                              ne0,
                              ne1])

    final_d = np.vstack((d.T,
                         d_atleast1_rev_per_paper.T,
                         d_atleast1_paper_per_rev.T,
                         d0,
                         d1))

    return v, final_ne, final_d


def create_assignment(x, a):
    """"given a solution `x` to the linear programming problem for paper assignments with cost matrix `a`,
    produce the actual assignment matrix b"""
    npapers = a.shape[0]
    nreviewers = a.shape[1]

    i, j = a.nonzero()

    t = np.array(x > 0.5).flatten()

    b = np.zeros((npapers, nreviewers))
    b[i[t], j[t]] = 1

    return b
"""Compute affinity matrices based on texts or other inputs"""

__all__ = ['compute_affinity']

import analyze_caption_topic as act
from gensim import corpora
import numpy as np
import scipy.sparse
from sklearn import decomposition


def compute_affinity(reviewers_abstracts, paper_abstracts, method='PCA'):
    """Compute the affinity matrix between reviewers and papers based on the abstracts
    and the method specified in `method` = {'PCA' (default)}"""

    # put all abstracts in one list
    all_abstracts = np.hstack((reviewers_abstracts,
                               paper_abstracts))

    all_texts = act.documents_to_texts(all_abstracts)
    dictionary = corpora.Dictionary(all_texts)                      # generate dictionary
    dictionary.filter_extremes(no_below=4, no_above=0.4)            # filter dictionary
    dictionary.compactify()                                         # compact dictionary
    all_corpus = [dictionary.doc2bow(text) for text in all_texts]   # get training corpus

    if method == 'PCA':

        # compute dtf matrix
        dtf_matrix = scipy.sparse.dok_matrix((dictionary.num_docs, len(dictionary.values())))
        for i in range(len(all_corpus)):
            for j, v in all_corpus[i]:
                dtf_matrix[i, j] = v

        dtf_dense = np.array(dtf_matrix.todense())

        pca_model = decomposition.PCA()
        pca_model.fit(dtf_dense)

        # how many components we will use for the analysis
        n_components = 10
        transf = pca_model.transform(dtf_matrix.todense())[:, 0:n_components]

        reviewers_dist = transf[0:len(reviewers_abstracts), :]
        paper_dist = transf[len(reviewers_abstracts):, :]
        from sklearn.neighbors import NearestNeighbors

        nbrs = NearestNeighbors(n_neighbors=reviewers_dist.shape[0]).fit(reviewers_dist)
        nn_distances, indices = nbrs.kneighbors(paper_dist)
        distances = np.zeros(nn_distances.shape)
        for i in range(distances.shape[0]):
            distances[i][indices[i]] = nn_distances[i]

        # set affinity matrix to the negative distance between reviewers and papers
        a = -distances

    else:
        raise Exception("Method `%s` uknown")

    return a
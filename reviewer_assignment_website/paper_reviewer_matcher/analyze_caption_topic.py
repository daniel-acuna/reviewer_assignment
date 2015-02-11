__author__ = 'titipat'

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import gensim
from gensim import corpora, models
import gensim.parsing
from sklearn import cross_validation
from unidecode import unidecode

#### FUNCTION ####

def documents_to_texts(docs):
    ''' Create list of texts from documents '''
    texts = []
    for j in range(len(docs)):
        texts.append(gensim.parsing.preprocess_string(docs[j], filters=[lambda x: x.lower(),
                                                                        unidecode,
                                                                        gensim.parsing.strip_tags,
                                                                        gensim.parsing.strip_punctuation,
                                                                        gensim.parsing.strip_multiple_whitespaces,
                                                                        gensim.parsing.strip_numeric,
                                                                        gensim.parsing.remove_stopwords,
                                                                        gensim.parsing.strip_short,
                                                                        gensim.parsing.stem_text]))
    # return texts list as output
    return texts


def compute_word_dist(lda, corpus):
    ''' Given LDA and testing corpus, compute most probable 10 words '''
    t_dist = lda.inference([corpus])[0].flatten()                       # topic distribution
    sum_tdist = np.sum(lda.inference([corpus])[0].flatten())
    t_distn = t_dist / sum_tdist                                        # normailze topic distribution
    tw_dist = lda.state.get_lambda()                                    # word distribution given topic
    tw_distn = tw_dist / np.atleast_2d(np.sum(tw_dist, axis=1)).T
    p_w = np.fliplr([np.sort(t_distn.dot(tw_distn))]).flatten()[0:10]   # print 10 words
    w_max = [dictionary.id2token[i] for i in np.fliplr([np.argsort(t_distn.dot(tw_distn))]).flatten()[0:10]]

    return pd.DataFrame(np.vstack([w_max, p_w]).T)

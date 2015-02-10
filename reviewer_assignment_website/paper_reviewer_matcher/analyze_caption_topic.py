__author__ = 'titipat'

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cv2
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


# #### CODE ####

# data = pd.read_csv('image_captions.csv')                        # load caption document data
# data = data.rename(columns={data.columns[0]: 'id'})             # rename column
# data_train, data_cv = cross_validation.train_test_split(data, test_size=0.15)  # split to training and testing
# data_train = pd.DataFrame(data_train, columns=list(data.columns)).fillna('')
# data_cv = pd.DataFrame(data_cv, columns=list(data.columns)).fillna('')

# captions = list(data_train.img_title + ' ' + data_train.img_caption)  # get all captions
# texts = documents_to_texts(captions)                            # create list of text from document

# dictionary = corpora.Dictionary(texts)                          # generate dictionary
# dictionary.filter_extremes(no_below=2, no_above=0.4)            # filter dictionary
# dictionary.compactify()                                         # compact dictionary

# corpus_train = [dictionary.doc2bow(text) for text in texts]     # get training corpus
# tfidf_train = models.TfidfModel(corpus_train)                   # generate tfidf model from existing corpus

# # train lda using term-frequency-idf or corpus itself
# lda = gensim.models.ldamodel.LdaModel(corpus=corpus_train, id2word=dictionary,
#                                       num_topics=300, alpha='auto',
#                                       iterations=2000,
#                                       update_every=1, chunksize=2000,
#                                       passes=10)

#### DISPLAY TESTING SET ####

def display_lda(index):
    preds = pd.DataFrame(lda[corpus_cv[index]], columns=['num_topic', 'value']).sort(['value'], ascending=False)
    preds = list(preds.num_topic[0:5])

    print captions_cv[index], '\n'
    print texts_cv[index], '\n'
    print 'Ten words with highest probability: \n', compute_word_dist(lda, corpus_cv[index]), '\n'
    print preds[0:5], '\n'
    print 'Selected topic: ', preds
    for pred in preds:
        print lda.print_topic(pred, topn=8)

    img = cv2.imread(data_cv.dir[index])
    plt.imshow(img)
    plt.axis('off')
    plt.show()

# example display

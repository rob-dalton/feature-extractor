import math
import string
import numpy as np

class Polarizer(object):
    """ Class to calculate polarity/semantic orientation of a document """

    def __init__(self, vocab, occurrence_matrix, pos_words, neg_words):
        self.vocab = vocab
        self.occurrence_matrix = occurrence_matrix
        self.num_docs = self.occurrence_matrix.shape[1]

        # NOTE: pos_words and neg_words should only contain terms that appear
        #       in vocab
        self.pos_words = pos_words
        self.neg_words = neg_words

    def get_document_polarity(self, doc):
        """ Get polarity of document """
        # filter doc to words in vocab
        # TODO: Justify this mathematically
        doc_words = (w.strip(string.punctuation).lower() for w in doc.split())

        polarity = 0
        num_words = 0
        for w in doc_words:
            if w in self.vocab:
                num_words += 1
                polarity += self._get_word_polarity(w)

        if num_words > 0:
            return polarity / num_words

    def _pmi(self, word1, word2):
        """ Get PMI of word1 and word2 """

        # find P(word1)
        p_word1 = self._count_occurrences(word1) / self.num_docs
        p_word2 = self._count_occurrences(word2) / self.num_docs

        # find P(word1 and word2)
        p_joint = self._count_co_occurrences(word1, word2) / self.num_docs
        if p_joint == 0:
            # NOTE: This assumes a base occurrence frequency of 1 in order to not break the PMI equation
            p_joint = 1 / self.num_docs

        return math.log(p_joint / (p_word1 * p_word2))

    def _get_word_polarity(self, word):
        """ Get polarity of word using pos, neg words """

        # get avg pos PMI
        pos_pmi = 0
        for pos_word in self.pos_words:
            pos_pmi += self._pmi(word, pos_word)

        pos_pmi = pos_pmi / len(self.pos_words)

        # get avg neg PMI
        neg_pmi = 0
        for neg_word in self.neg_words:
            neg_pmi += self._pmi(word, neg_word) / 2

        neg_pmi = neg_pmi / len(self.neg_words)

        return pos_pmi - neg_pmi

    def _get_vocab_index(self, word):
        for i, w in enumerate(self.vocab):
            if w == word:
                return i

    def _count_occurrences(self, word):
        i = self._get_vocab_index(word)
        if i is None:
            return 0
        else:
            return np.sum(self.occurrence_matrix[i])

    def _count_co_occurrences(self, word1, word2):
        """ Count number of documents that contain word1 and word2 """

        # get vocab indices
        i_word1 = self._get_vocab_index(word1)
        i_word2 = self._get_vocab_index(word2)

        # get co_occurrence_vector, return sum
        if i_word1 and i_word2:
            co_occurrence_vector = np.multiply(self.occurrence_matrix[i_word1],
                                               self.occurrence_matrix[i_word2].transpose())
            return np.sum(co_occurrence_vector)

        return 0

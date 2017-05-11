# -*- coding: utf-8 -*-

from gensim.models import word2vec
import logging

def main():

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
	
    sentences = word2vec.Text8Corpus("wiki_seg.txt")
    model = word2vec.Word2Vec(sentences, size=260)
    # ## save model 1
    # model.save_word2vec_format(u"wiki.zh.model.bin", binary=True)
    # ## save model 2
    model.save('wiki.zh.model')

    # ## load model 1
    # model = word2vec.Word2Vec.load_word2vec_format("wiki.zh.model.bin", binary=True)
	# ## load model 2
	# model = word2vec.Word2Vec.load('wiki.zh.model')

if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-

from gensim.models import word2vec
import logging

def main():

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
	
    sentences = word2vec.Text8Corpus("wiki_seg.txt")
    model = word2vec.Word2Vec.load('wiki.zh.model')
    model.train(sentences, total_examples = model.corpus_count, epochs=model.iter)

if __name__ == "__main__":
    main()

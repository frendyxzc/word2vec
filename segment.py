# -*- coding: utf-8 -*-

import jieba
import logging
import io

def main():

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    # load stopwords set
    stopwordset = set()
    with io.open('jieba_dict/stopwords_zh.txt','r',encoding='utf-8') as sw:
        for line in sw:
            stopwordset.add(line.strip('\n'))

    texts_num = 0

    output = io.open('wiki_seg.txt','w',encoding='utf-8')
    with io.open('wiki_texts_zh.txt','r',encoding='utf-8') as content :
        for line in content:
            words = jieba.cut(line, cut_all=False)
            for word in words:
                if word not in stopwordset:
                    output.write(word +' ')

            texts_num += 1
            if texts_num % 10000 == 0:
                logging.info("分词已完成前 %d 行" % texts_num)
    output.close()

if __name__ == '__main__':
    main()

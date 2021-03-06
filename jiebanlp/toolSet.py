#encoding=utf8
__author__ = 'jdwang'
__date__ = 'create date: 2016-05-15'
import numpy as np
import logging
import timeit
import jieba
import jieba.posseg as jseg
import os
import re
import io

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

jieba.load_userdict(os.path.dirname(__file__)+'/userdict.txt')
logging.debug('='*20)
logging.debug('加载stopwords列表....')
stopword_list = io.open(os.path.dirname(__file__)+'/stopword.txt','r',encoding='utf8').read().strip().split()

logging.debug(u'stopwords有：%s'%(','.join(stopword_list)))
logging.debug('='*20)
exclude_word_list = set(['886','88'])
logging.debug(u'exclude words有：%s'%(','.join(exclude_word_list)))
logging.debug('='*20)


def pos_seg(word):
    # for items in jseg.lcut(word):
    #     print items.flag,items.word

    return jseg.lcut(word)[0].flag


def seg(sentence,sep='|',full_mode = True,remove_stopword = False):
    '''
    使用jieba分词进行分词
    :param sentence: 待分词句子
    :type sentence: str
    :param remove_stopword: 是否去除stopword
    :type remove_stopword: bool
    :return:返回分词后字符串,seg_srt
    :rtype: str
    '''
    # logging.debug('是否去除stopwords：%s'%remove_stopword)
    # for items in jseg.lcut(sentence):
    #     print items.flag,items.word

    seg = []
    pattern = re.compile('[0-9]+$')
    for items in jseg.lcut(sentence):
        # 利用词性标注去除标点符号
        if items.flag == 'x':
            logging.debug(u'句子（%s）将标点符号："%s"替换成""'%(sentence,items.word))
            seg.append('')
            # continue
        if remove_stopword and items.word in stopword_list:
            logging.debug(u'句子（%s）去除stopwords：%s' % (sentence,items))
            continue
        # 将数字替换成 NUM
        if pattern.match(items.word) and items.word not in exclude_word_list:
            print items
            seg.append('DIGITTAG')
            logging.debug(u'句子（%s）将数字："%s" 替换成标记："DIGITTAG"'%(sentence,items.word))
        else:
            seg.append(items.word)
    # sentence = [items.word for items in jseg.lcut(sentence) if items.flag!='x']


    sentence = ' '.join(seg)
    # print sentence
    # print sentence
    seg_list = jieba.lcut(sentence, cut_all=full_mode)
    # print seg_list
    seg_list = [item for item in seg_list if len(item.strip())!=0]
    # print seg_list
    seg_srt = sep.join(seg_list)
    return seg_srt

if __name__ == '__main__':
    sent = u'还有什么别的要求吗，没了'
    sent = u'有哪些1000块的手机适合我'
    print seg(sent,sep='|',full_mode=False)
    # print seg(sent,sep='|',full_mode=True)

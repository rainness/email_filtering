#! /usr/bin/python

import sys
import os
import jieba
import build_model
reload(sys)
sys.setdefaultencoding('utf-8')

def judge(word_dict, msg, threshold, top_k):
    word_prob = dict()
    seg_array = jieba.cut(msg)
    for word in seg_array:
        if (word_prob.has_key(word)):
            continue
        else:
            if word_dict.has_key(word):
                word_prob[word] = word_dict[word]
    sorted(word_prob.iteritems(), key = lambda d:d[1], reverse = True)
    positive_val = 1.0
    negative_val = 1.0
    cnt = 0
    for key, value in word_prob.items():
        positive_val *= float(value)
        negative_val *= (1 - float(value))
        cnt += 1
        if cnt >= top_k:
            break
    predict_val = positive_val / (positive_val + negative_val)
    if (predict_val >= threshold):
        return True
    else:
        return False
            
def predict(word_dict, file_path, threshold, top_k):
    reader = open(file_path, 'r')
    sentence = ""
    while True:
        line = reader.readline()
        if not line:
            break
        sentence += line
    reader.close()
    return judge(word_dict, sentence, threshold, top_k)

if __name__ == "__main__":
    model_path = sys.argv[1]
    detect_path = sys.argv[2]
    threshold = sys.argv[3]
    top_k = sys.argv[4]
    word_dict = build_model.load_model(model_path)
    is_Spam = predict(word_dict, detect_path, threshold, top_k)
    print is_Spam

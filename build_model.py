#! /usr/bin/python

import sys
import os
import jieba
reload(sys)
sys.setdefaultencoding('utf-8')

def recursively_dir(root_dir):
    file_list = list()
    for file_or_dir in os.listdir(root_dir):
        file_or_dir_tmp = os.path.join(root_dir, file_or_dir)
        if os.path.isdir(file_or_dir_tmp):
            file_list.extend(recursively_dir(file_or_dir_tmp))
        else:
            file_list.append(file_or_dir_tmp)
    return file_list

def load_index(index_file):
    print "loading index indicating spam or not..."
    spam_set = list()
    prefix = os.path.dirname(os.path.abspath(index_file))
    reader = open(index_file, 'r')
    while True:
        line = reader.readline()
        if not line:
            break
        array = line.strip().split(' ')
        if (array[0] == "spam"):
            filename = array[1].replace("../", "")
            spam_set.append(filename)
    print "index loading finished..."        
    return spam_set

def is_spam(index_list, filename):
    try:
        index_list.index(filename)
        return True
    except:
        return False

def parse(root_dir, index):
    word_map = dict()
    print "starting to scan all files..."
    file_list = recursively_dir(root_dir)
    print "file scaning finished..."
    index_list = load_index(index)
    cnt = 0
    spam_cnt = 0
    total_cnt = 0
    for filename in file_list:
        word_unique_for_file = set()
        Is_spam = is_spam(index_list, filename)
        if Is_spam:
            spam_cnt += 1
        total_cnt += 1    
        reader = open(filename, 'r')
        while True:
            line = reader.readline()
            if not line:
                break
            seg_array = jieba.cut(line)
            for word in seg_array:
                word_unique_for_file.add(word)
            for word in word_unique_for_file:
                if (word_map.has_key(word)):
                    if Is_spam:
                        word_map[word][1] += 1
                    else:
                        word_map[word][0] += 1
                else:
                    if Is_spam:
                        word_map.setdefault(word, [0, 1])
                    else:
                        word_map.setdefault(word, [1, 0])
        reader.close()
        cnt += 1
        if (cnt % 1000 == 0):
            print str(cnt) + " files has been segmented already!"
    word_map.setdefault('ALL', [total_cnt - spam_cnt, spam_cnt])
    print "all files has been handled already, the total number is: " + str(cnt) + "..."
    print "the total word is: " + str(len(word_map)) + "..."
    return word_map

def cal_word_spam_prob(ham_prob, spam_prob, ham_word_prob, spam_word_prob):
    return spam_prob * spam_word_prob / (ham_prob * ham_word_prob + spam_prob * spam_word_prob)

def is_regular_word(word):
    try:
        word.decode("utf-8")
        return True
    except:
        return False

def save_model(word_dict, model_path):
    print "start to model saving to file..."
    writer = open(model_path, 'w')
    total_val = word_dict.pop('ALL')
    ham_cnt = float(total_val[0])
    spam_cnt = float(total_val[1])
    ham_prob = ham_cnt / (ham_cnt + spam_cnt)
    spam_prob = spam_cnt / (ham_cnt + spam_cnt)
    for key, value in word_dict.items():
        ham_word_cnt = value[0]
        spam_word_cnt = value[1]
        ham_word_prob = float(ham_word_cnt) / float(ham_cnt)
        spam_word_prob = float(spam_word_cnt) / float(spam_cnt)
        if ham_word_prob == 0.0:
            ham_word_prob = 0.01
        if spam_word_prob == 0.0:
            spam_word_prob = 0.01
        word_spam_prob = cal_word_spam_prob(ham_prob, spam_prob, ham_word_prob, spam_word_prob)    
        writer.write(key + "\t" + str(word_spam_prob) + "\n")
    writer.close()
    print "model has been saved to local file:" + model_path

def build_model(root_dir, index_path, model_path):
    word_dict = parse(root_dir, index_path)
    save_model(word_dict, model_path)

def load_model(model_path):
    word_prob = dict()
    reader = open(model_path, 'r')
    while True:
        line = reader.readline()
        if not line:
            break
        array = line.split('\t')
        try:
            word = array[0]
            prob = float(array[1])
            word_prob[word] = prob
        except:
            print array
    reader.close()
    return word_prob

if __name__ == "__main__":
    input_dir = sys.argv[1]
    index_path = sys.argv[2]
    model_path = sys.argv[3]
    build_model(input_dir, index_path, model_path)

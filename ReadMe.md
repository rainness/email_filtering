# Email_Filtering using machine learning

## ================================

## Introduction

It mainly used for spam email detection using Naive Bayes

## Build

$ git clone https://github.com/rainness/email_filtering.git

## Quick Start

$ pip install jieba / pip3 install jieba

$ wget http://plg.uwaterloo.ca/cgi-bin/cgiwrap/gvcormac/trec06c.tgz

$ tar -zxvf trec0c

$ cd email_filtering

$ cp -r trec06c/data . 

$ cp -r trec06c/full/index .

$ python build_model.py data index model

$ python predict.py model test_email 0.9 10

## License

Copyright 2016 Rainness individual.

Licensed under the Apache License, Version 2.0: http://www.apache.org/licenses/LICENSE-2.0

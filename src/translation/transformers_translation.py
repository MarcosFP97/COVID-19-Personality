#!/usr/bin/env python
# coding: utf-8


import dask
import dask.dataframe as dd
import re

tweets_df1 = dd.read_csv('tweets_sampled_es.csv',       
                    usecols = ['tweet', 'language', 'date'])

tweets=tweets_df1.reset_index(drop=True)
tweets=tweets.loc[tweets['language']=='es']
tweets=tweets.loc[:, ['date', 'tweet']]
tweets=tweets.reset_index(drop=True) 

def tweetClean(tuit):
    tuit = str(tuit)
    tuit = re.sub('(www|https)[^\s]+', ' ', tuit)
    tuit = re.sub('#', ' ', tuit)
    tuit = re.sub('@', ' ', tuit)
    return tuit

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch,tensorflow 
device = "cuda:0" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-es-en")
model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-es-en").to(device) 

def translate(text):
    tokenized_text = tokenizer([text], return_tensors='pt',max_length=512,truncation=True).to(device) 
    return tokenizer.batch_decode(model.generate(**tokenized_text), skip_special_tokens=True)[0]


tweets['tweet'] = tweets['tweet'].map(lambda x: tweetClean(x))
tweets['tweet'] = tweets['tweet'].map(lambda x: translate(x))
tweets.to_csv('tweets_sampled_es_en.csv', single_file=True) 








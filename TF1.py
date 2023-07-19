#!/usr/bin/env python
# coding: utf-8

# In[1]:


import findspark
findspark.init()
import pyspark
import sys
import re
from pyspark import SparkContext
from operator import add
from math import log
sc = SparkContext("local","Task1a")
rdd1 = sc.textFile(sys.argv[1])
#rdd1 = sc.textFile("C:/Users/nandh/OneDrive/Desktop/CloudComputing/UpdatedCode/CC_Project/Project_Data")
rdd2 = rdd1.map(lambda x : x.split("</title>"))
def clean(x):
    res = []
    stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
    punctuations = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    line = re.sub('<.*?>','',x[0])
    str1 = x[1].lower()
    str1 = re.sub('\[?(?:https?|ftp):\/\/[\n\S]+(\])?','',str1)
    str1 = re.sub('<.*?>','',str1)
    str1 = re.sub('\[\[.*?\]\]','',str1)
    for p in punctuations:
        str1 = str1.replace(p,'')
    str1 = ' '.join([word for word in str1.split() if word not in stop_words])
    str1 = str1.split()
    for i in str1:
        res.append((i,line,1))
    return(res)
rdd3 = rdd2.flatMap(clean).map(lambda x : ((x[0],x[1]),x[2])).reduceByKey(add).map(lambda x : (x[0],1+log(x[1],10))).map(lambda x : (x[0][0],((x)[0][1],x[1]))).groupByKey()
def output_file(lines):
    str2 = ''  
    for j in lines:
        str2 = str2 + j[0] + '#' + str(j[1]) + '+'
    return(str2[:-1])
rdd3.map(lambda x : (x[0] + '@' + output_file(x[1]))).saveAsTextFile(sys.argv[2])


# In[ ]:





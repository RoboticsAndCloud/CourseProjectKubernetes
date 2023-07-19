#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import findspark
findspark.init()
import pyspark
import sys
from pyspark import SparkContext
global count
import re
from operator import add
sc = SparkContext('local',"Task1b")
count = 0
#rdd1 = sc.textFile("TF_index")
rdd1 = sc.textFile(sys.argv[1])
def retransform(x):
    y=x.split("@")
    z=y[1].split("+")
    aList = []
    for list in z:
        k=list.split("#")
        aList.append(k)
    return (y[0], aList)
rdd2 = rdd1.map(retransform)
f_name = open(sys.argv[2],'r')
#f_name = open("Desktop/Sample.txt")
for line in f_name:
    count = count + 1
    query = line
    if query == '':
        break
    query_dict = {}
    query_dict[count] = query
    query1 = list(query_dict.items())
    rdd3 = sc.parallelize(query1)
    def clean(x):
        punctuations ='!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
        stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
        str1 = x.lower()
        str1 = re.sub('\[?(?:https?|ftp):\/\/[\n\S]+(\])?','',str1)
        str1 = re.sub('<.*?>','',str1)
        for p in punctuations:
            str1 = str1.replace(p, '')
        str1 = ' '.join([word for word in str1.split() if word not in stopwords])
        str1 = str1.split()
        return str1
    rdd4 = rdd3.map(lambda x : (x[0],clean(x[1])))
    rdd5 = rdd4.flatMap(lambda x : x[1]).collect()
    rdd6 = rdd2.filter(lambda x : x[0] in rdd5)
    rdd6.flatMap(lambda x: x[1]).reduceByKey(add).sortBy(lambda a : a[1],ascending=False).map(lambda x : x[0]).zipWithIndex().filter(lambda b : b[1] < 10).keys().coalesce(1).saveAsTextFile("TFQID - "+str(count))
f_name.close()


#!/usr/bin/env python
# coding: utf-8

# In[1]:


import bz2
import xml.etree.ElementTree as ET
import string
import os
import re


# In[3]:

print("Started Data Parsing")
file_path = '/app_data/simplewiki-20200301-pages-articles.xml.bz2'
output_dir = '/app_data/AssignmentData_Latest/'


# In[ ]:


# Parse the input and get only required fields
# Organize in <title>DOC TITLE</title><text>Document content</text>
doc_count = 0
doc_title = ''

print_count = 0

with bz2.BZ2File(file_path,mode='r') as f:
    parser = ET.iterparse(f, events=('start', 'end'))
    
    for event, element in parser:        
        if element.tag == '{http://www.mediawiki.org/xml/export-0.10/}title' and event == 'end':
            doc_title = element.text
        if element.tag == '{http://www.mediawiki.org/xml/export-0.10/}text' and event == 'end':
            if os.path.exists(output_dir + str(doc_count) + '.txt'):
                doc_count += 1
                continue
            else:
                try:
                    text = element.text.replace('\n',' ')
                    op = open(output_dir + str(doc_count) + '.txt','w')
                    op.write('<title>' + doc_title.encode('ascii',errors='ignore').decode() + '</title><text>' + text.encode('ascii',errors='ignore').decode() + '</text>')
                    op.close()
                    doc_title = ''
                    doc_count += 1
                except Exception as e:
                    doc_title = ''
                    continue


# In[11]:


# To group multiple documents into one document
# After grouping the document will be of format:
    # <title>DOC1</title><text>DOC1 content</text>
    # <title>DOC2</title><text>DOC2 content</text>
    # <title>DOC3</title><text>DOC3 content</text>
    # .....
    # .....


final_output_path = '/app_data/Final_CombinedData/'
# final_output_path = 'C:/Users/abagava/Downloads/Assignment3Data_tiny/'

files = os.listdir(output_dir)
to_write = ''
docs_written = 0

def write_func(file_name,content):
    op = open(final_output_path + str(file_name) + '.txt','w')
    op.write(content)
    op.close()

# Write 10000 documents into one
for i,f in enumerate(files):
    if i % 10000 == 0:
#     if i == 2000:
        write_func(docs_written,to_write)
        docs_written += 1
        to_write = ''
#         break
        
    fp = open(output_dir + f,'r')
    for j,line in enumerate(fp):
        to_write += line + '\n'
    fp.close()
    
write_func(docs_written,to_write)
print("Data parse complete")


# In[ ]:





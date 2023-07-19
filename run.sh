#!/bin/bash
nohup python /code/parse_wikipedia_data.py > parsedata.out 2>&1 &
wait $!
nohup mkdir /projectdata && cp /app_data/Final_CombinedData/1.txt /projectdata && cp /app_data/Final_CombinedData/2.txt /projectdata && cp /app_data/Final_CombinedData/3.txt /projectdata > datacopy.out 2>&1 &
wait $!
nohup python /code/TF1.py /projectdata /project_TFIndex  > TFindex.out 2>&1 &
wait $!
nohup python /code/TF1_query.py /project_TFIndex /code/Sample.txt > TFQuery.out 2>&1 &
while true; do sleep 1000; done
wait $!
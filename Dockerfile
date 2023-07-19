FROM ubuntu
MAINTAINER  Raj
RUN apt-get update
RUN apt-get install -y default-jdk default-jre 
RUN apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip 
RUN apt-get -y install vim
RUN apt-get install -y wget dos2unix

RUN mkdir spark
RUN wget http://apache.mirrors.hoobly.com/spark/spark-3.0.0-preview2/spark-3.0.0-preview2-bin-hadoop2.7.tgz
RUN tar -xzvf spark-3.0.0-preview2-bin-hadoop2.7.tgz -C /spark

ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH=$PATH:$JAVA_HOME/bin
ENV SPARK_HOME=/spark/spark-3.0.0-preview2-bin-hadoop2.7
ENV PATH=$PATH:$SPARK_HOME/bin
RUN pip install findspark

#Downloading data from wikipedia dumps
RUN mkdir app_data
RUN wget https://dumps.wikimedia.org/simplewiki/20200301/simplewiki-20200301-pages-articles.xml.bz2
RUN mv simplewiki-20200301-pages-articles.xml.bz2 /app_data
RUN mkdir /app_data/AssignmentData_Latest/
RUN mkdir /app_data/Final_CombinedData/
RUN mkdir code
COPY ./parse_wikipedia_data.py /code
COPY ./TF1.py /code
COPY ./TF1_query.py /code
COPY ./Sample.txt /code
COPY ./run.sh /code

RUN chmod +x /code/run.sh
RUN dos2unix /code/run.sh
CMD /code/run.sh

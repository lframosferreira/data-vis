FROM ubuntu
FROM python:3.10.12

WORKDIR /app

RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN apt-get install -y git

RUN git clone https://github.com/lframosferreira/data-vis.git
WORKDIR /app/data-vis

RUN rm data/spadl_format/France_matches.csv
RUN rm data/spadl_format/France.csv
RUN rm data/spadl_format/Germany_matches.csv
RUN rm data/spadl_format/Germany.csv
RUN rm data/spadl_format/Italy_matches.csv
RUN rm data/spadl_format/Italy.csv
RUN rm data/spadl_format/Spain_matches.csv
RUN rm data/spadl_format/Spain.csv

RUN pip install -r requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:9000", "main:server"]
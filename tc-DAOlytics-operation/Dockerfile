FROM python:3.10-bullseye AS base

# RUN apt-get update && apt-get -y upgrade

WORKDIR /project

COPY . . 

RUN pip3 install -r requirements.txt

CMD ["python3", "start_rabbit_mq.py"]
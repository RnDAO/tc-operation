FROM python:3.10 AS test

RUN apt-get update && apt-get -y upgrade

ADD . /root/home/tc-DAOlytics-ops/

ADD tc-DAOlytics/analyzer/requirements.txt /root/home/requirements.txt

RUN pip3 install /root/home/tc-DAOlytics-ops/tc-DAOlytics/analyzer/

RUN pip3 install -r /root/home/requirements.txt

RUN pip3 install tc-messageBroker

CMD ["python3", "/root/home/tc-DAOlytics-ops/start_rabbit_mq.py"]
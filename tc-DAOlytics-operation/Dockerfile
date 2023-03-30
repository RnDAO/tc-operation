FROM python:3.10

RUN apt-get update && apt-get -y upgrade

ARG ssh_prv_key
ARG ssh_pub_key

EXPOSE 8080

# Authorize SSH Host
RUN mkdir -p /root/.ssh && \
    chmod 0700 /root/.ssh && \
    ssh-keyscan github.com > /root/.ssh/known_hosts

# Add the keys and set permissions
RUN echo "$ssh_prv_key" > /root/.ssh/id_rsa && \
    echo "$ssh_pub_key" > /root/.ssh/id_rsa.pub && \
    chmod 600 /root/.ssh/id_rsa && \
    chmod 600 /root/.ssh/id_rsa.pub

WORKDIR "/var/www/analyzer"

COPY ./tc-DAOlytics/analyzer/requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN rm -rf /root/.ssh/

RUN rm -rf requirements.txt

COPY ./tc-DAOlytics/ .

COPY ./start.py ./analyzer/rndao_analyzer/start.py

CMD [ "python3", "./analyzer/rndao_analyzer/start.py"]

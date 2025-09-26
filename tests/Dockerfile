FROM ubuntu:22.04

RUN apt update && \
    apt install -y \
        python3 \
        pip \
        make

COPY ./requirements.txt /opt

RUN pip3 install -r /opt/requirements.txt && \
    rm /opt/requirements.txt

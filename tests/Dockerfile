FROM ubuntu:22.04

COPY ./assets/scripts/apt-install.sh /opt
COPY ./assets/requirements.txt /opt

RUN chmod +x -R /opt

RUN /opt/apt-install.sh && \
    rm /opt/apt-install.sh

RUN pip3 install -r /opt/requirements.txt && \
    rm /opt/requirements.txt

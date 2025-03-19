FROM python:3

RUN apt-get -y update \
    && apt-get -y install sudo \
    && pip install scapy \
    && apt -y install libpcap0.8 \
    && apt-get -y install net-tools

RUN apt-get -y install nano

WORKDIR /usr/src/app

COPY inquisitor.py .
COPY pop.py .

# Set executable permissions for pop.py
RUN chmod +x pop.py

CMD ["tail", "-f", "/dev/null"]
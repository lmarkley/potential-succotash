FROM ubuntu:latest

RUN apt update && apt install python3 python3-pip -y

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY test_suite.py /root/test_suite.py 
COPY api_calls.py /root/api_calls.py

WORKDIR /root
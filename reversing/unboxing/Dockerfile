FROM debian:buster-slim

ARG port

RUN apt-get update -y; apt-get install python3 python3-pip socat build-essential libffi-dev -y
RUN pip3 install --upgrade pip && pip3 install keystone-engine
RUN mkdir /unboxing
ADD chall.py /unboxing/chall.py
ADD flag.txt /unboxing/flag.txt

EXPOSE $port

ENTRYPOINT ["socat", "-s", "TCP-LISTEN:11002,reuseaddr,fork", "EXEC:timeout 5m python3 /unboxing/chall.py,stderr"]
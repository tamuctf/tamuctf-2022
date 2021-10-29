FROM debian:buster-slim

ARG port

RUN apt-get update -y; apt-get install python3 python3-pip socat -y
RUN python3 -m pip install networkx
RUN mkdir /labyrinth
ADD chall.py /labyrinth/chall.py
ADD flag.txt /labyrinth/flag.txt

EXPOSE $port

ENTRYPOINT ["socat", "-s", "TCP-LISTEN:11000,reuseaddr,fork", "EXEC:timeout 5m python3 /labyrinth/chall.py,stderr"]
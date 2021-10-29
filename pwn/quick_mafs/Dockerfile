FROM debian:buster-slim


RUN apt-get update -y; apt-get install socat python3 build-essential -y
ADD chall.py /pwn/chall.py
ADD flag.txt /pwn/flag.txt
WORKDIR /pwn

EXPOSE 11001

ENTRYPOINT ["socat", "-s", "TCP-LISTEN:11001,reuseaddr,fork", "EXEC:timeout 10m python3 /pwn/chall.py,stderr"]

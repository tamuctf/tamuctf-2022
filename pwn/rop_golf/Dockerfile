FROM debian:buster-slim as build

ARG name

RUN apt-get update -y; apt-get install build-essential -y
ADD $name.c /tmp/$name.c
ADD Makefile /tmp/Makefile
RUN cd /tmp/; make all

FROM debian:buster-slim

ARG name
ARG port

RUN apt-get update -y; apt-get install socat -y
RUN mv /usr/bin/socat /socat
COPY --from=build /tmp/$name /pwn/$name
COPY flag.txt /pwn/flag.txt
RUN mv /pwn/flag.txt /pwn/$(tr -dc 'A-F0-9' < /dev/urandom | head -c32).txt
WORKDIR /pwn

EXPOSE $port

RUN rm /usr/bin/*; rm /sbin/*; rm /usr/sbin/*; rm /bin/*;

ENTRYPOINT ["/socat", "-s", "TCP-LISTEN:7002,reuseaddr,fork", "EXEC:/pwn/rop_golf,stderr"]
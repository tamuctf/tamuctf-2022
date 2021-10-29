FROM alpine as build

RUN apk add alpine-sdk
ADD *.c *.h /tmp/
ADD Makefile /tmp/Makefile
RUN cd /tmp/; make all

FROM scratch

ARG name
ARG port

COPY --from=build /tmp/tcp-server /pwn/tcp-server
COPY --from=build /tmp/$name /pwn/$name
COPY flag.txt /pwn/flag.txt

EXPOSE $port

ENTRYPOINT ["/pwn/tcp-server"]

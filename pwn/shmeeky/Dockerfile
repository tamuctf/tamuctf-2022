FROM debian:bookworm-slim

RUN apt-get update -y && apt-get install -y socat qemu-system procps

RUN mkdir /pwn

WORKDIR /pwn

ADD flag.txt flag.txt
ADD start.sh start.sh
ADD run_socat.sh run_socat.sh
ADD bzImage bzImage
ADD rootfs.cpio rootfs.cpio
RUN chmod +x start.sh
RUN chmod +x run_socat.sh

EXPOSE 7007
CMD ["/pwn/run_socat.sh"]
FROM ubuntu:18.04 as build

RUN apt update; apt -y --autoremove full-upgrade
RUN DEBIAN_FRONTEND=noninteractive apt install -y git curl autoconf automake autotools-dev curl libmpc-dev libmpfr-dev libgmp-dev libusb-1.0-0-dev gawk build-essential bison flex texinfo gperf libtool patchutils bc zlib1g-dev device-tree-compiler pkg-config libexpat-dev autoconf automake autotools-dev curl python3 libmpc-dev libmpfr-dev libgmp-dev gawk build-essential bison flex texinfo gperf libtool patchutils bc zlib1g-dev libexpat-dev

RUN mkdir -p /opt/riscv
RUN mkdir -p /opt/riscv-build
WORKDIR /opt/riscv-build

ENV RISCV=/opt/riscv
RUN git clone https://github.com/riscv/riscv-gnu-toolchain
WORKDIR /opt/riscv-build/riscv-gnu-toolchain

RUN ./configure --prefix=$RISCV && \
    make -j$(nproc)

WORKDIR /opt/riscv-build
RUN git clone --recursive https://github.com/riscv-software-src/riscv-isa-sim.git
RUN mkdir riscv-isa-sim/build
WORKDIR /opt/riscv-build/riscv-isa-sim/build
RUN mkdir -p /opt/out
RUN ../configure --prefix=/opt/out && \
    make -j$(nproc) && \
    make install

FROM ubuntu:18.04

RUN apt update; apt -y --autoremove full-upgrade
RUN DEBIAN_FRONTEND=noninteractive apt install -y socat device-tree-compiler sudo

COPY --from=build /opt/out /usr/
COPY run.sh /usr/bin/run.sh
COPY flag.txt /root/flag.txt

RUN useradd -ms /bin/bash pwn
ADD pwn-sudoer /etc/sudoers.d/00-pwn

USER pwn
ENTRYPOINT ["sh", "-c", "exec socat TCP-LISTEN:1800,reuseaddr,fork EXEC:'/usr/bin/run.sh',stderr"]

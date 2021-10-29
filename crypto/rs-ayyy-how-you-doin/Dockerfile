FROM rust as build

ADD src /opt/rs-ayyy-how-you-doin/src
ADD Cargo.toml /opt/rs-ayyy-how-you-doin/Cargo.toml
ADD flag.txt /opt/rs-ayyy-how-you-doin/flag.txt

WORKDIR /opt/rs-ayyy-how-you-doin

RUN cargo build --release

FROM ubuntu

RUN apt update; apt -y install socat
COPY --from=build /opt/rs-ayyy-how-you-doin/target/release/rs-ayyy-how-you-doin /usr/bin/rs-ayyy-how-you-doin

EXPOSE 8320

ENTRYPOINT ["sh", "-c", "exec socat -d -d TCP-LISTEN:8320,reuseaddr,fork EXEC:'timeout 5m rs-ayyy-how-you-doin',stderr"]

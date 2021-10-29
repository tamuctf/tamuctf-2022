FROM ekidd/rust-musl-builder as build

ADD Cargo.toml Cargo.toml
ADD Cargo.lock Cargo.lock
ADD src/ src/
RUN cargo build --release --bin sokorazy

FROM scratch

COPY --from=build /home/rust/src/target/x86_64-unknown-linux-musl/release/sokorazy /sokorazy

EXPOSE 7304

ENTRYPOINT ["/sokorazy"]

ARG BOOTSTRAP_IMAGE=golang:1.17.13-bullseye@sha256:c10d8b1987ad5ddf7816d2f3a56e4a58b5826285dc1449edbb061b3aad25648b
FROM ${BOOTSTRAP_IMAGE} AS bootstrap

FROM debian:bookworm-slim@sha256:99c0b25c46d0214d5a2091092e7908907dcaecd6a962cde0ac700acee222b6f3
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates git gcc g++ libc6-dev make pkg-config \
    && rm -rf /var/lib/apt/lists/*
COPY --from=bootstrap /usr/local/go /opt/bootstrap

# Original source immediately before the logger-isolation fix.
ARG UPSTREAM_REVISION=28a6f9cf2bccaabc69e7beb3d86161fa77f21daf
ARG TOOLCHAIN_BUILD_JOBS=4
RUN git init /opt/go \
    && git -C /opt/go remote add origin https://github.com/golang/go.git \
    && git -C /opt/go fetch --depth=1 origin "$UPSTREAM_REVISION" \
    && git -C /opt/go checkout --detach FETCH_HEAD \
    && test "$(git -C /opt/go rev-parse HEAD)" = "$UPSTREAM_REVISION"
WORKDIR /opt/go/src
RUN GOROOT_BOOTSTRAP=/opt/bootstrap GOTOOLCHAIN=local GOMAXPROCS=$TOOLCHAIN_BUILD_JOBS \
    CGO_ENABLED=1 ./make.bash
RUN mkdir -p /work
ENV PATH=/opt/go/bin:$PATH GOROOT=/opt/go GOTOOLCHAIN=local GOENV=off
RUN mkdir -p /scratch

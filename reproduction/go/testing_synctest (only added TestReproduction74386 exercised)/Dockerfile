ARG BOOTSTRAP_IMAGE=golang:1.24.6-bookworm@sha256:ab1d1823abb55a9504d2e3e003b75b36dbeb1cbcc4c92593d85a84ee46becc6c
FROM ${BOOTSTRAP_IMAGE} AS bootstrap

FROM debian:bookworm-slim@sha256:99c0b25c46d0214d5a2091092e7908907dcaecd6a962cde0ac700acee222b6f3
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates git gcc g++ libc6-dev make pkg-config \
    && rm -rf /var/lib/apt/lists/*
COPY --from=bootstrap /usr/local/go /opt/bootstrap

# Original source before the synctest WaitGroup lifetime fix.
ARG UPSTREAM_REVISION=4731832342f6430d6eb4cb13a00b97c3db5da993
ARG TOOLCHAIN_BUILD_JOBS=4
RUN git init /opt/go \
    && git -C /opt/go remote add origin https://github.com/golang/go.git \
    && git -C /opt/go fetch --depth=1 origin "$UPSTREAM_REVISION" \
    && git -C /opt/go checkout --detach FETCH_HEAD \
    && test "$(git -C /opt/go rev-parse HEAD)" = "$UPSTREAM_REVISION"
WORKDIR /opt/go/src
RUN GOROOT_BOOTSTRAP=/opt/bootstrap GOTOOLCHAIN=local GOMAXPROCS=$TOOLCHAIN_BUILD_JOBS \
    CGO_ENABLED=1 ./make.bash
ENV PATH=/opt/go/bin:$PATH GOROOT=/opt/go GOTOOLCHAIN=local GOENV=off
RUN mkdir -p /scratch

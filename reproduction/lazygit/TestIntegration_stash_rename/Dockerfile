FROM golang:1.24.0-bookworm@sha256:b970e6d47c09fdd34179acef5c4fecaf6410f0b597a759733b3cbea04b4e604a
# Original source before stash-rename rendering was deferred.
ARG UPSTREAM_REVISION=c55062fe86775815d45af5ec7b7011a7ce4b8ca8
ARG BUILD_JOBS=2
RUN git init /opt/upstream && git -C /opt/upstream remote add origin https://github.com/jesseduffield/lazygit.git \
    && git -C /opt/upstream fetch --depth=1 origin "$UPSTREAM_REVISION" && git -C /opt/upstream checkout --detach FETCH_HEAD
WORKDIR /opt/upstream
ENV GOTOOLCHAIN=local GOENV=off GOFLAGS=-mod=vendor GOMAXPROCS=$BUILD_JOBS CGO_ENABLED=0
RUN mkdir -p /tmp/lazygit \
    && go build -p="$BUILD_JOBS" -o /tmp/lazygit/test_lazygit pkg/integration/clients/injector/main.go \
    && go build -p="$BUILD_JOBS" -o /opt/integration-cli cmd/integration_test/main.go

FROM golang:1.25.0-bookworm@sha256:81dc45d05a7444ead8c92a389621fafabc8e40f8fd1a19d7e5df14e61e98bc1a
# Original source before stale diff-task results were rejected.
ARG UPSTREAM_REVISION=f063832dd35821e3c2112342cf60b5669e7f2fde
ARG BUILD_JOBS=2
RUN git init /opt/upstream && git -C /opt/upstream remote add origin https://github.com/jesseduffield/lazygit.git \
    && git -C /opt/upstream fetch --depth=1 origin "$UPSTREAM_REVISION" && git -C /opt/upstream checkout --detach FETCH_HEAD
WORKDIR /opt/upstream
ENV GOTOOLCHAIN=local GOENV=off GOFLAGS=-mod=vendor GOMAXPROCS=$BUILD_JOBS CGO_ENABLED=0
RUN command -v script && command -v stty \
    && mkdir -p /tmp/lazygit \
    && go build -p="$BUILD_JOBS" -o /tmp/lazygit/test_lazygit pkg/integration/clients/injector/main.go \
    && go build -p="$BUILD_JOBS" -o /opt/integration-cli cmd/integration_test/main.go \
    && test -z "$(git status --porcelain)"
ENTRYPOINT ["bash"]

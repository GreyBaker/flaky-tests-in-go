FROM golang:1.20.3-bullseye@sha256:595c9af0430dd84bad33020e7e9e328af4bd1a1aabd46a03b5bf6f252cdbecf3 AS historical_go
FROM golang:1.24.0-bookworm@sha256:b970e6d47c09fdd34179acef5c4fecaf6410f0b597a759733b3cbea04b4e604a
COPY --from=historical_go /usr/local/go /opt/go120
ENV PATH=/opt/go120/bin:${PATH} GOROOT=/opt/go120
# Original conflict/patch fixtures before their synchronization fix.
ARG UPSTREAM_REVISION=275ed1248657b85d40a77683db42e013295d64cf
ARG BUILD_JOBS=2
RUN git init /opt/upstream && git -C /opt/upstream remote add origin https://github.com/jesseduffield/lazygit.git \
    && git -C /opt/upstream fetch --depth=1 origin "$UPSTREAM_REVISION" && git -C /opt/upstream checkout --detach FETCH_HEAD
WORKDIR /opt/upstream
ENV GOTOOLCHAIN=local GOENV=off GOFLAGS=-mod=vendor GOMAXPROCS=$BUILD_JOBS CGO_ENABLED=0 \
    GIT_CONFIG_GLOBAL=/opt/upstream/test/global_git_config
RUN test "$(go version)" = 'go version go1.20.3 linux/amd64' \
    && test "$(git config --get user.name)" = CI \
    && test "$(git config --get user.email)" = CI@example.com \
    && mkdir -p /tmp/lazygit \
    && go build -p="$BUILD_JOBS" -o /tmp/lazygit/test_lazygit pkg/integration/clients/injector/main.go \
    && go build -p="$BUILD_JOBS" -o /opt/integration-cli cmd/integration_test/main.go

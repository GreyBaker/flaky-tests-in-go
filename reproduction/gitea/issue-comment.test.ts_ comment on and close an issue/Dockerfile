# syntax=docker/dockerfile:1
FROM golang:1.26.3-bookworm@sha256:386d475a660466863d9f8c766fec64d7fdad3edac2c6a05020c09534d71edb4b AS go
FROM node:24-bookworm@sha256:e7add2a490bb17d97b485b8641bd88455fff7839ade0f5eba493c3508124d413
COPY --from=go /usr/local/go /usr/local/go
ARG BUILD_JOBS=2
ARG TEST_UID=1000
ARG TEST_GID=1000
ENV PATH=/usr/local/go/bin:$PATH GOTOOLCHAIN=local GOENV=off GOFLAGS=-mod=readonly GOMAXPROCS=$BUILD_JOBS PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
RUN apt-get update && apt-get install -y --no-install-recommends git-lfs
RUN git init /src && git -C /src remote add origin https://github.com/go-gitea/gitea.git \
 && git -C /src fetch --depth=1 origin b4407e36aae31a1a48b285446eff07515f6deab1 && git -C /src checkout --detach FETCH_HEAD
WORKDIR /src
RUN npm install -g "$(node -p 'JSON.parse(require("fs").readFileSync("package.json")).packageManager')" \
 && pnpm install --frozen-lockfile && make frontend
RUN pnpm exec playwright install --with-deps firefox \
 && make generate-backend && go build -p="$BUILD_JOBS" -o /src/gitea .
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright PLAYWRIGHT_MODE=local EXECUTABLE=gitea CI=true
RUN chown -R "$TEST_UID:$TEST_GID" /src

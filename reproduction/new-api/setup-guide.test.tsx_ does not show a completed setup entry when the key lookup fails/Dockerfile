FROM oven/bun:1.4.0-debian@sha256:5bb0f9be3a1a36a03e27c9a9dd894a3b1ad26657155c7df4dda771e17bf872ef AS bun
FROM node:24-bookworm@sha256:e7add2a490bb17d97b485b8641bd88455fff7839ade0f5eba493c3508124d413
ARG REVISION=7fd06381976cbea126d1f20973548bf60f20e37d
RUN apt-get update && apt-get install -y --no-install-recommends python3
COPY --from=bun /usr/local/bin/bun /usr/local/bin/bun
RUN git init /src && git -C /src remote add origin https://github.com/QuantumNous/new-api.git \
    && git -C /src fetch --depth=1 origin "$REVISION" && git -C /src checkout --detach FETCH_HEAD
WORKDIR /src/web
RUN --mount=type=cache,id=newapi-bun140,target=/root/.bun/install/cache \
    bun install --frozen-lockfile && test -z "$(git status --porcelain)" \
    && mkdir -p node_modules/.vite node_modules/.vite-temp

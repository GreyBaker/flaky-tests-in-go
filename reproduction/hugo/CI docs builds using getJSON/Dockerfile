FROM golang:1.15.15-buster@sha256:414340e7bfee1b13c72c59e9b0df5488b83b6a5c99c2d806509304ca7ef71350
RUN git init /src && git -C /src remote add origin https://github.com/gohugoio/hugo.git \
 && git -C /src fetch --depth=1 origin 8cbe2bbfad6aa4de267921e24e166d4addf47040 && git -C /src checkout --detach FETCH_HEAD
WORKDIR /src
RUN git submodule update --init --recursive && go build -tags extended -o /opt/hugo .

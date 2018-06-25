FROM alpine:3.7

RUN apk add --no-cache curl python

ENTRYPOINT ["/usr/bin/curl"]

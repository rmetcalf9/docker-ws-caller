FROM alpine:3.7

RUN apk add --no-cache curl python

COPY ./scripts/kong_install_service_and_route /usr/bin

RUN chmod +x /usr/bin/kong_install_service_and_route

ENTRYPOINT ["/usr/bin/curl"]

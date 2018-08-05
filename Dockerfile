FROM alpine:3.8

RUN apk add --no-cache curl python python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

COPY ./scripts/kong_install_service_and_route /usr/bin
COPY ./scripts/kong_install_consumer_with_api /usr/bin

RUN chmod +x /usr/bin/kong_install_service_and_route
RUN chmod +x /usr/bin/kong_install_consumer_with_api

ENTRYPOINT ["/bin/sh"]

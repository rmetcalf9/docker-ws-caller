FROM alpine:3.8

RUN apk add --no-cache curl python python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    pip3 install requests && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

COPY ./scripts/* /usr/bin/


RUN chmod +x /usr/bin/kong_install_service_and_route && \
    chmod +x /usr/bin/kong_install_consumer_with_api && \
    chmod +x /usr/bin/kong_delete_service && \
    chmod +x /usr/bin/kong_add_route_to_service && \
    chmod +x /usr/bin/kong_delete_all_certs && \
    chmod +x /usr/bin/kong_update_cert_where_any_snis_match && \
    chmod +x /usr/bin/kong_test && \
    chmod +x /usr/bin/kong_add_upstream && \
    chmod +x /usr/bin/kong_delete_all_routes_apart_from_one && \
    chmod +x /usr/bin/kong_update_or_add_cert_where_any_snis_match


#Features to add
# Connect test endpoint to new container
# If main service dosen't exist create it
# Add new container as upstream to main service
# Move main service so it is 100% pointing at new service


ENTRYPOINT ["/bin/sh"]

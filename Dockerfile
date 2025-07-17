FROM alpine:3.16.0

RUN apk add --no-cache curl python3 gcc python3-dev linux-headers build-base libffi-dev ack entr rsync openssh-client sed && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    pip3 install requests && \
    pip3 install nose && \
    pip3 install rednose && \
    pip3 install docker && \
    pip3 install beautifulsoup4 && \
    pip3 install lxml && \
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
    chmod +x /usr/bin/kong_add_jwt_and_acl_plugins && \
    chmod +x /usr/bin/kong_update_or_add_cert_where_any_snis_match && \
    chmod +x /usr/bin/docker_helloworld && \
    chmod +x /usr/bin/docker_service_remove_non_live && \
    chmod +x /usr/bin/transferDirectory && \
    chmod +x /usr/bin/rdockerinit


#Features to add
# Connect test endpoint to new container
# If main service dosen't exist create it
# Add new container as upstream to main service
# Move main service so it is 100% pointing at new service


ENTRYPOINT ["/bin/sh"]


## docker run --rm --name docker_ws_caller --mount type=bind,source=$(pwd),target=/ext_volume metcarob/docker-ws-caller:latest -c "echo abc"
## docker run --rm --name docker_ws_caller -it --mount type=bind,source=$(pwd),target=/ext_volume metcarob/docker-ws-caller:latest

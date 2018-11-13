# docker-ws-caller
Docker image with curl and python installed which I can use to call web services

# Test Kong server

A lot of these scripts operate on a Kong image. For development a local test Kong server can be started with the following commands:

```
docker stack deploy --compose-file=docker-compose-test-instance.yml tmp-kong-stack
```

Konga will be at
127.0.0.1:1337

Kong admin is at
127.0.0.1:8001

See scripts for usage examples




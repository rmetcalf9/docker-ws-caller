#!/bin/sh

DATADIR="./kong_stack_for_test/data/1.1.2"

if [ ! -d ${DATADIR} ]; then
  mkdir -p ${DATADIR}
fi

COMPOSEFILE=./kong_stack_for_test/docker-compose.yml
if [ $# -eq 1 ]; then
  COMPOSEFILE=${1}
  echo "Using non standard compose ${COMPOSEFILE}"
fi
docker stack deploy --compose-file=${COMPOSEFILE} kongforautotest

# If network dosen't exist
# docker network create --driver=overlay --attachable tmp-kong-stack --opt encrypted

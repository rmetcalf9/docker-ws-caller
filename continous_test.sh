#!/bin/sh

#export KONGVER="0.13.1"
export KONGVER="1.1.2"


TESTFILE=all
if [ $# -gt 0 ]; then
  TESTFILE=${1}
  echo "Setting test file to ${TESTFILE}"
fi

if [ "E${2}" = "Edocker" ]; then
  docker run --rm --network tmp-kong-stack -e KONGTESTURL=http://kong:8001 -e KONGVER=${KONGVER} -it --mount type=bind,source=$(pwd),target=/ext_volume metcarob/docker-ws-caller:0.5.1 /ext_volume/zz_continous_test.sh /ext_volume ${TESTFILE}
  exit 0
fi

export KONGTESTURL=http://127.0.0.1:8381

./zz_continous_test.sh ./ ${TESTFILE}

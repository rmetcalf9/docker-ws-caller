
TESTFILE=all
if [ $# == 1 ]; then
  echo "Setting test file to ${TESTFILE}"
  TESTFILE=${1}
fi

if [ ${1} == "docker" ]; then
  docker run --rm --network tmp-kong-stack -e KONGTESTURL=http://kong:8001 -it --mount type=bind,source=$(pwd),target=/ext_volume metcarob/docker-ws-caller:0.5.0 /ext_volume/zz_continous_test.sh /ext_volume ${TESTFILE}
  exit 0
fi

export KONGTESTURL=http://127.0.0.1:8381

./zz_continous_test.sh ./ ${TESTFILE}


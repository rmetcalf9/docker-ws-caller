#!/bin/sh

echo 'To test one file pass filename as first param'
echo 'e.g. sudo ./continous_test.sh test_JobExecution.py'

if [ $# -ne 2 ]; then
  echo "Wrong number of params passed"
  echo "Need:"
  echo " 1. root dir"
  echo " 2. test file to run or 'all' for all"
fi

CURDIR=${1}
TESTFILE=${2}


cd ${1}

##export KONGTESTURL=http://ansiblerunner:8381

#Sometimes kong server not responding first time from python
#  for an unknown reason this corrects that
wget -qO- ${KONGTESTURL} > /dev/null
RES=$?
if [[ ${RES} -ne 0 ]]; then
  echo "wget against ${KONGTESTURL} failed"
  exit ${RES}
fi
echo "wget check passed"


if [[ E${TESTFILE} == "Eall" ]]; then
  echo "Normal Ver"
  until ack -f ./scripts ./test | entr -d nosetests --rednose ./test; do sleep 1; done
else
  echo "Single file version"
  until ack -f ./scripts ./test | entr -d nosetests --rednose ${1}; do sleep 1; done
fi

#docker run --rm --network tmp-kong-stack -e KONGTESTURL=http://kong:8001 --mount type=bind,source=$(pwd),target=/ext_volume metcarob/docker-ws-caller:0.4.2 /ext_volume/continous_test.sh /ext_volume all


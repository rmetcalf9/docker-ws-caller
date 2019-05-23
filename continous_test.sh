#!/bin/bash

echo 'To test one file pass filename as first param'
echo 'e.g. sudo ./continous_test.sh test_JobExecution.py'

if [ $# -eq 2 ]; then
  echo "Passed input param, going to change into ${2}"
  cd ${2}
fi

##export KONGTESTURL=http://ansiblerunner:8381

#Sometimes kong server not responding first time from python
#  for an unknown reason this corrects that
wget -qO- ${KONGTESTURL} > /dev/null



if [ $# -gt 0 ]; then
  until ack -f --python  ./scripts ./test | entr -d nosetests --rednose ./test; do sleep 1; done
else
  until ack -f --python  ./scripts ./test | entr -d nosetests --rednose ${1}; do sleep 1; done
fi

#docker run --rm --network tmp-kong-stack -e KONGTESTURL=${KONGTESTURL} --mount type=bind,source=$(pwd),target=/ext_volume metcarob/docker-ws-caller:0.3.6 /ext_volume/continous_test.sh /ext_volume


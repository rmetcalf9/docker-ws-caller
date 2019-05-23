#!/bin/bash

echo 'To test one file pass filename as first param'
echo 'e.g. sudo ./continous_test.sh test_JobExecution.py'


#Sometimes kong server not responding first time from python
#  for an unknown reason this corrects that
wget -qO- http://127.0.0.1:8381 > /dev/null



if [ $# -eq 0 ]; then
  until ack -f --python  ./scripts ./test | entr -d nosetests --rednose ./test; do sleep 1; done
else
  until ack -f --python  ./scripts ./test | entr -d nosetests --rednose ${1}; do sleep 1; done
fi


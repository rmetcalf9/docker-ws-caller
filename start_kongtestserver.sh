
COMPOSEFILE=./kong_stack_for_test/docker-compose.yml
if [ $# -eq 1 ]; then
  COMPOSEFILE=${1}
  echo "Using non standard compose ${COMPOSEFILE}"
fi
docker stack deploy --compose-file=${COMPOSEFILE} kongforautotest

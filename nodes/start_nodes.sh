#!/bin/bash

onred='\033[41m'
ongreen='\033[42m'
onyellow='\033[43m'
endcolor='\033[0m'

# Handle errors
set -e
error_report() {
    echo -e "${onred}Error: start_nodes.sh failed on line $1.$endcolor"
}
trap 'error_report $LINENO' ERR

if [ ! -z "$DLMNET" ] && [ $DLMNET==TESTNET ]; then
    ocean=nile
    echo -e "${onyellow}Starting nodes on testnet...$endcolor"
else
    ocean=spree
    echo -e "${onyellow}Starting nodes for local testing...$endcolor"
fi

cd oef-core
./oef-core-image/scripts/docker-run.sh -p 3333:3333 -- &> /dev/null &

cd ../barge
./start_ocean.sh --latest --no-pleuston --no-brizo --local-$ocean-node --force-pull &> /dev/null &

while [ $id!="" ]; do
    id=$(docker container ls | grep ocean_ | awk '{print $1}')
    sleep 5
done

echo -e "${ongreen}Nodes started.$endcolor"

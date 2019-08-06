#!/bin/bash

onred='\033[41m'
ongreen='\033[42m'
onyellow='\033[43m'
endcolor='\033[0m'

# Handle errors
set -e
error_report() {
    echo -e "${onred}Error: start_nodes.sh failed on line $1. Ensure you have started Docker.$endcolor"
}
trap 'error_report $LINENO' ERR

if [ "$NET" == "MAIN" ]; then
    ocean=pacific
    echo -e "${onyellow}Starting nodes on mainnet...$endcolor"
elif [ "$NET" == "TEST" ]; then
    ocean=nile
    echo -e "${onyellow}Starting nodes on testnet...$endcolor"
else
    ocean=spree
    echo -e "${onyellow}Starting nodes for local testing...$endcolor"
fi

cd oef-search-pluto
python3 scripts/launch.py -c ./scripts/launch_config.json --background &> /dev/null
cd ../oef-mt-core
bazel run mt-core/main/src/cpp:app -- --config_file `pwd`/mt-core/main/src/cpp/config.json &> /dev/null &

cd ../barge
./start_ocean.sh --latest --no-pleuston --no-aquarius --no-brizo --no-secret-store --no-faucet --local-$ocean-node &> /dev/null &

while [ $id!="" ]; do
    id=$(docker container ls | grep ocean_ | awk '{print $1}')
    sleep 5
done

echo -e "${ongreen}Nodes started.$endcolor"

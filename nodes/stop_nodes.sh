#!/bin/bash

onred='\033[41m'
ongreen='\033[42m'
onyellow='\033[43m'
endcolor="\033[0m"

# Handle errors
set -e
error_report() {
    echo -e "${onred}Error: stop_nodes.sh failed on line $1.$endcolor"
}
trap 'error_report $LINENO' ERR

echo -e "${onyellow}Stopping nodes...$endcolor"

#docker stop $(docker ps | grep oef-core-pluto-image | awk '{ print $1 }')

docker stop $(docker ps | grep ocean_ | awk '{ print $1 }')

echo -e "${ongreen}Nodes stopped.$endcolor"

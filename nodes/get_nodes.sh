#!/bin/bash

onred='\033[41m'
ongreen='\033[42m'
onyellow='\033[43m'
endcolor="\033[0m"

# Handle errors
set -e
error_report() {
    echo -e "${onred}Error: get_nodes.sh failed on line $1.$endcolor"
}
trap 'error_report $LINENO' ERR

# Script functions
get_latest() {
    if [ ! -d $2 ]; then
        git clone https://github.com/$1/$2.git --recursive
        cd $2
    else
        cd $2
        git pull
    fi
    cd ..
}

# Install requirements
echo -e "${onyellow}Installing Ocean Node...$endcolor"
get_latest oceanprotocol barge
mv barge ocean_node

echo -e "${onyellow}Installing Fetch Node...$endcolor"
get_latest fetchai oef-core 
mv oef-core fetch_node
cd fetch_node
./oef-core-pluto-image/scripts/docker-build-img.sh

echo -e "${ongreen}Nodes installed.$endcolor"

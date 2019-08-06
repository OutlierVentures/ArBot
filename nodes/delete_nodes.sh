#!/bin/bash

onred='\033[41m'
ongreen='\033[42m'
onyellow='\033[43m'
endcolor='\033[0m'

# Handle errors
set -e
error_report() {
    echo -e "${onred}Error: get_nodes.sh failed on line $1.$endcolor"
}
trap 'error_report $LINENO' ERR

rm -rf barge oef-mt-core oef-search-pluto

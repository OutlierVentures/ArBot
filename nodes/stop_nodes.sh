#!/bin/bash

ongreen='\033[42m'
onyellow='\033[43m'
endcolor='\033[0m'

echo -e "${onyellow}Stopping nodes...$endcolor"

docker stop $(docker ps | grep oef | awk '{ print $1 }')

docker stop $(docker ps | grep ocean_ | awk '{ print $1 }')

echo -e "${ongreen}Nodes stopped.$endcolor"

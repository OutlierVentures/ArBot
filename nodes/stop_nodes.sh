#!/bin/bash

ongreen='\033[42m'
onyellow='\033[43m'
endcolor='\033[0m'

echo -e "${onyellow}Stopping nodes...$endcolor"

docker stop $(docker ps -a | grep oef-search | awk '{print $1}') &> /dev/null
kill -INT $(ps | grep oef-mt-core | awk '{print $1}') &> /dev/null

docker stop $(docker ps -a | grep ocean_ | awk '{print $1}') &> /dev/null

echo -e "${ongreen}Nodes stopped.$endcolor"

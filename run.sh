#!/bin/bash

env=.dev
cmd=up

if [ $1 ]
then env=".$1"
fi

if [ $2 ]
then cmd="$2"
fi

command="docker-compose -f docker-compose$env.yml $cmd"

echo "Executing $command"
$command
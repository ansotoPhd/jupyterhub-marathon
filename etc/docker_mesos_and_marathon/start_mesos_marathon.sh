#!/usr/bin/env bash

dir=$(dirname "$0")
docker-compose -f $dir/docker-compose.yml up

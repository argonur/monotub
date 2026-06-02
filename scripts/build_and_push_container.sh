#!/bin/bash

set -e

docker build -t argonur/finances:fenrir-dev .
docker push argonur/finances:fenrir-dev
#!/bin/sh

working_directory=$1
fedora_version=$2

image_name="hid-nx__rpm-packaging__fc$fedora_version"

docker build -t $image_name --build-arg FEDORA_VERSION=$fedora_version -f packaging/fedora/Dockerfile .
docker run --rm -v $working_directory:/github/workspace $image_name

#!/bin/bash

version=$(grep '"version"' metadata.json | awk -F ':' '{print $2}' |  tr -d '", ')
collector_base_image_name="devo.com/ifc_base"
collector_base_image_latest_version="latest"
collector_base_image_now_version=$(date +%s)

collector_name=$(grep '"package_name"' metadata.json | awk -F ':' '{print $2}' |  tr -d '", ')
docker_base_image=$(docker image ls ${collector_base_image_name}:${collector_base_image_latest_version} | grep ${collector_base_image_name} | awk -F ' ' '{print $1 ":" $2}')

echo -e "Docker image base: \"${docker_base_image}\""
if [ "$docker_base_image" == "" ]; then
  echo -e "\nBuilding the base Docker image ($collector_base_image_name:$collector_base_image_latest_version)"
  docker build --platform linux/amd64 --progress plain --compress --force-rm --no-cache --file Dockerfile.base --tag ${collector_base_image_name}:latest .
  docker tag ${collector_base_image_name}:latest ${collector_base_image_name}:${collector_base_image_latest_version}
fi

echo -e "\nBuilding the Docker image (devo.com/collectors/$collector_name:$version)"
docker build --platform linux/amd64 --progress plain  --compress --force-rm --no-cache --tag devo.com/collectors/${collector_name}:${version} .
if [ $? -eq 0 ]; then
   echo -e "\nSaving previously created Docker image to a .tgz file (filename: \"collector-$collector_name-docker-image-$version.tgz\")"
   docker save devo.com/collectors/${collector_name}:${version} | gzip > collector-${collector_name}-docker-image-${version}.tgz
else
   echo -e "\nPrevious build failed so the .tgz file containing the Docker image will not be created"
fi
#!/bin/bash

# remove not running containers
docker rm -f $(docker ps -f "status=exited" -q)

declare -A used_images

whitelisted_images="registry.access.redhat.com/openshift3/ose-sti-builder registry.access.redhat.com/openshift3/ose-deployer docker-registry.default.svc:5000/appdynamics/java-agent:20.8.0"

# collect images which has running container
for image in $(docker ps | awk 'NR>1 {print $2;}'); do
    id=$(docker inspect --format="{{.Id}}" $image);
    used_images[$id]=$image;
done

# append whitelisted images to used_images list

for whitelisted_image in $whitelisted_images; do
    wl_image_id=$(docker images | grep $whitelisted_image | awk '{print $3}');
    [[ "$wl_image_id" != "" ]] && id=$(docker inspect --format="{{.Id}}" $wl_image_id) && used_images[$id]=$whitelisted_image;
done

# loop over images, delete those without a container
for id in $(docker images --no-trunc -q); do
    if [ -z ${used_images[$id]} ]; then
        echo "images is NOT in use: $id" >> imagesnotinuse_$(date +%Y%m%d-%H%M).log
        docker rmi $id -f
        if [ $? > 0 ]; then
        echo "images cannot be deleted: $id" >> imagescantdel_$(date +%Y%m%d-%H%M).log
        fi
    else
        echo "images is in use:     ${used_images[$id]}" >> imagesinuse__$(date +%Y%m%d-%H%M).log
    fi
done

find /root/ -name "imagesinuse*.log" -mtime +30 -exec rm -rf {} \;
find /root/ -name "imagescantdel*.log" -mtime +30 -exec rm -rf {} \;
find /root/ -name "imagesnotinuse*.log" -mtime +30 -exec rm -rf {} \;

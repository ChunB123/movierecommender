#!/bin/bash

reload_nginx() {
  docker exec nginx /usr/sbin/nginx -s reload
}

zero_downtime_deploy() {
  service_name=inference-service
  old_container_id=$(docker ps -f name=$service_name -q | tail -n1)
  # bring a new container online, running new code
  # (nginx continues routing to the old container only)
  docker compose up -d --build $service_name --no-deps --scale $service_name=2 --no-recreate $service_name
  sleep 3
  # start routing requests to the new container (as well as the old)
  reload_nginx
  # take the old container offline
  docker stop $old_container_id
  docker rm $old_container_id
  docker compose up -d --no-deps --scale $service_name=1 --no-recreate $service_name
  # stop routing requests to the old container
  reload_nginx
}
zero_downtime_deploy
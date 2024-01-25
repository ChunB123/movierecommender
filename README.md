# Movie Recommendation System
Provide live recommendations for 1 million users from 27k movies. 


## For remote machine
``
ssh team-2@fall2023-comp585-2.cs.mcgill.ca
``

Check current movielog 
``
docker run -it --log-opt max-size=50m --log-opt max-file=5 bitnami/kafka kafka-console-consumer.sh --bootstrap-server fall2023-comp585.cs.mcgill.ca:9092 --topic movielog2
``

Check movielog from beginning
``
docker run -it --log-opt max-size=50m --log-opt max-file=5 bitnami/kafka kafka-console-consumer.sh --bootstrap-server fall2023-comp585.cs.mcgill.ca:9092 --topic movielog2 --from-beginning
``

Is the server still live?
``
http://fall2023-comp585-2.cs.mcgill.ca:8082/recommend/1
``

`
docker run -it -p 8082:8082/tcp chunb123/ml_service:v0`

`docker ps`

`docker stop <container_id_or_name>`

`docker rm <container_id_or_name>`



## Retrive Data
``curl http://fall2023-comp585.cs.mcgill.ca:8080/user/1``

``curl http://fall2023-comp585.cs.mcgill.ca:8080/movie/turistas+2006``


## For local machine
Update requirements.txt (independencies) for docker
`
pip freeze > requirements.txt
`

Test Locally (Rebuild after changing the requirements.txt)
```bash
docker compose up --build
```
```bash
docker compose up --build inference-service
```
```bash
docker compose down -v
```
```bash
docker compose rm -f -s -v inference-service
```
```bash
curl http://localhost:8082/recommend/1
```


## For Deployment
Check CPU, RAM and NET resources
```
docker stats
```

## Bash Script for Zero downtime
```bash
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
```
Start inference-service
```bash
docker compose up -d --build inference-service --no-deps --scale inference-service=1 --no-recreate inference-service
```
Start nginx and inference-service
```bash
docker compose up --build inference-service nginx
```
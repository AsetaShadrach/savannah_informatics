#!/bin/bash

docker run -p 127.0.0.1:7999:8080 -e KC_BOOTSTRAP_ADMIN_USERNAME=admin -e KC_BOOTSTRAP_ADMIN_PASSWORD=admin quay.io/keycloak/keycloak:26.3.4 start-dev

cd inventory_service
docker build -t savdjango . && docker run -p 8000:8000 --net=host -d savdjango
cd ..
cd gateway_service
docker build -t knd_gateway .  && docker run -p 9090:9090 --net=host -d knd_gateway

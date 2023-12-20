#!/usr/bin/make
build:
	docker build -t gd_traffic_proxy:latest .

run:
	docker-compose up \
		gd_traffic_proxy


run-bg:
	docker-compose up -d \
		gd_traffic_proxy

stop:
	docker-compose down

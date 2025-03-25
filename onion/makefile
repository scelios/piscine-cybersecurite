# ---------------------------------------------------------------------------- #
#                                    DEFINS                                    #
# ---------------------------------------------------------------------------- #
NAME	:= inquisitor.py
TARGET	:= inquisitor

SERVER	:= server
CLIENT	:= client

CYAN="\033[1;36m"
RED="\033[31m"
GREEN="\033[32m"
YELLOW="\033[33m"
RESET="\033[m"

# ---------------------------------------------------------------------------- #
#                                     RULES                                    #
# ---------------------------------------------------------------------------- #

build:
	docker build -t onion_project .

.PHONY: all
all	: 
	docker run -p 8080:80 -p 4343:4242 --name onion_container onion_project

exec:
	docker exec -it onion_container /bin/bash

.PHONY: clean
clean	:
	docker stop onion_container
	docker rm onion_container

.PHONY: prune
prune	: clean
	-docker system prune -f -a

.PHONY: fclean
fclean	: clean
	-docker stop $(shell docker ps -qa) 2>/dev/null
	-docker rm $(shell docker ps -qa) 2>/dev/null
	-docker rmi -f $(shell docker images -qa) 2>/dev/null
	-docker volume rm $(shell docker volume ls -q) 2>/dev/null
	-docker network rm $(shell docker network ls -q) 2>/dev/null
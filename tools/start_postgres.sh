#!/bin/bash

#no permanent storage
docker run \
  -d \
  --name postgresql \
  -p 5432:5432 \
  -e POSTGRES_PASSWORD=somePassword \
  postgres:13-alpine


#with local storage
#docker run \
#  -d \
#  --name postgresql \
#  -p 5432:5432 \
#  -e POSTGRES_PASSWORD=somePassword \
#  -v /home/<your_user_id_here>/pgdata:/var/lib/postgresql/data \
#  postgres:13-alpine

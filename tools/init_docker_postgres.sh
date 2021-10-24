#!/bin/bash
#note, username must be UNIQUE , if not primary key
docker exec postgresql psql -U postgres -c "CREATE TABLE birthdays (username VARCHAR(255) PRIMARY KEY, birth_date DATE NOT NULL);"
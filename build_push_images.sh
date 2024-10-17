#!/bin/bash

cd data-populator
docker build -t juanroldan1989/data-populator .
docker push juanroldan1989/data-populator
cd ../data-query
docker build -t juanroldan1989/data-query .
docker push juanroldan1989/data-query
cd ../flask
docker build -t juanroldan1989/flask .
docker push juanroldan1989/flask
cd ../nginx
docker build -t juanroldan1989/nginx .
docker push juanroldan1989/nginx

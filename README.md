# FastAPI using Docker

[![Docker Repository on Quay](https://quay.io/repository/laurobmb/python_fastapi/status "Docker Repository on Quay")](https://quay.io/repository/laurobmb/python_fastapi)

![Docker Stars](https://img.shields.io/docker/stars/laurobmb/fastapi.svg)
![Docker Pulls](https://img.shields.io/docker/pulls/laurobmb/fastapi.svg)
![Docker Automated](https://img.shields.io/docker/automated/laurobmb/fastapi.svg)
![Docker Build](https://img.shields.io/docker/build/laurobmb/fastapi.svg)

This project is using FASTAPI inside a container. Just compile the Dockerfile and run it on the host

#### Build

> podman build -t fastapi:v1.0 .

or 

> docker build -t fastapi:v1.0 .

#### Execute

> podman run -it -p 8000:8000 fastapi:v1.0

or

> docker run -it -p 8000:8000 fastapi:v1.0

#### Kubernetes

> kubectl apply -f k8s/deployment.yaml

[github.com](https://github.com/laurobmb)
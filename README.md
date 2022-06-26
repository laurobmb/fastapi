# FastAPI using Docker

[![Docker Repository on Quay](https://quay.io/repository/laurobmb/python_fastapi/status "Docker Repository on Quay")](https://quay.io/repository/laurobmb/python_fastapi)
![Docker Stars](https://img.shields.io/docker/stars/laurobmb/fastapi.svg)
![Docker Pulls](https://img.shields.io/docker/pulls/laurobmb/fastapi.svg)
![Docker Automated](https://img.shields.io/docker/automated/laurobmb/fastapi.svg)
![Docker Build](https://img.shields.io/docker/build/laurobmb/fastapi.svg)

This project is using FASTAPI inside a container. Just compile the Dockerfile and run it on the host

#### Build
    podman build -t fastapi:v1.0 .
#### Execute
    podman run -it -p 8000:8000 fastapi:v1.0
#### Deploy Kubernetes with YAML
    kubectl apply -f k8s/deployment.yaml
#### Deploy OCP
    oc new-project fastapi
    
    oc new-app --name fastapi --labels app=fastapi https://github.com/laurobmb/fastapi.git#master --context-dir app --strategy=docker --env ENVIROMENT="prod"

    oc new-app --name fastapi --labels app=fastapi https://github.com/laurobmb/fastapi.git#master --context-dir app --strategy=source --env ENVIROMENT="prod"

    oc -n fastapi expose service fastapi
    
    oc -n fastapi expose service fastapi --name fastapi-hml --hostname fastapi-fastapi.hml.lagomes.rhbr-lab.com

    oc -n fastapi create secret generic fastapi-secret --from-literal=username=admin --from-literal=password=secret
    
    oc -n fastapi set env --from=secret/fastapi-secret deployment/fastapi

    oc -n fastapi set volume deployment/fastapi --name=secrets-vol --add --mount-path=/opt/secrets/ --secret-name=fastapi-secret --overwrite

    oc -n fastapi create configmap fastapi-page --from-literal=index.html='<!DOCTYPE html><html><h1><body>This is a configmap file from production environment</h1></html>'

    oc -n fastapi set volume deployment/fastapi --name=page-vol --add --mount-path=/opt/config/ --configmap-name=fastapi-page --overwrite



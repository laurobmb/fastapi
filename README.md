# FastAPI using Docker

[![Docker Repository on Quay](https://quay.io/repository/laurobmb/python_fastapi/status "Docker Repository on Quay")](https://quay.io/repository/laurobmb/python_fastapi)
![Docker Stars](https://img.shields.io/docker/stars/laurobmb/fastapi.svg)
![Docker Pulls](https://img.shields.io/docker/pulls/laurobmb/fastapi.svg)
![Docker Automated](https://img.shields.io/docker/automated/laurobmb/fastapi.svg)
![Docker Build](https://img.shields.io/docker/build/laurobmb/fastapi.svg)

This project is using FASTAPI inside a container. Just compile the Dockerfile and run it on the host

## Build
    podman build -t fastapi:v1.0 .
## Execute
    podman run -it -p 8000:8000 fastapi:v1.0
## Deploy Kubernetes with YAML
    kubectl apply -f k8s/deployment.yaml

## Deploy OCP

### Configurando projeto
    oc new-project fastapi
    
### Deploy     
    oc new-app --name fastapi --labels app=fastapi https://github.com/laurobmb/fastapi.git#master --context-dir app --strategy=docker --env ENVIROMENT="prod"

    oc new-app --name fastapi --labels app=fastapi https://github.com/laurobmb/fastapi.git#master --context-dir app --strategy=source --env ENVIROMENT="prod"

### Expor rota
    oc -n fastapi expose service fastapi
    
    oc -n fastapi expose service fastapi --name fastapi-hml --hostname fastapi-fastapi.hml.lagomes.rhbr-lab.com

    oc -n fastapi create route edge fastapi-tls --service fastapi

### Create secret
    oc -n fastapi create secret generic fastapi-secret --from-literal=username=admin --from-literal=password=secret
    
    oc -n fastapi set env --from=secret/fastapi-secret deployment/fastapi

    oc -n fastapi set volume deployment/fastapi --name=secrets-vol --add --mount-path=/opt/secrets/ --secret-name=fastapi-secret --overwrite

### Create configmap
    oc -n fastapi create configmap fastapi-page --from-literal=index.html='<!DOCTYPE html><html><h1><body>This is a configmap file from production environment</h1></html>'

    oc -n fastapi set volume deployment/fastapi --name=page-vol --add --mount-path=/opt/config/ --configmap-name=fastapi-page --overwrite

### Create resources limits
    oc -n fastapi set resources deployment/fastapi --limits=cpu=200m,memory=128Mi --requests=cpu=100m,memory=64Mi

    oc -n fastapi autoscale deployment fastapi --max 10 --min 3 --cpu-percent=80

    oc -n fastapi create quota fastapi-quota --hard=cpu=500m,memory=500Mi

### Create healthcheck
    oc -n fastapi set probe deployment/fastapi --readiness --initial-delay-seconds=10 --timeout-seconds=30 --get-url=http://:8080/health
    
    oc -n fastapi set probe deployment/fastapi --liveness --initial-delay-seconds=10 --timeout-seconds=30 --get-url=http://:8080/health
    
    


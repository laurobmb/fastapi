#!/bin/bash

echo "Buildando podman"
podman build -t fastapi:v1 .

echo "Parando container antigo"
podman stop fastapi

echo "Removendo container antigo"
podman rm fastapi

echo "Criando novo container de monitoramento"
podman run \
--add-host suassunapf:172.18.0.4 \
--dns-search=trf5.gov.br \
--dns-search=conectado.local \
--restart=on-failure \
--publish=8000:8000 \
--detach \
--name fastapi fastapi:v1 

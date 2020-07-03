# FastAPI using Docker

This project is using FASTAPI inside a container. Just compile the Dockerfile and run it on the host

#### Build

> podman build -t fastapi:v1.0 .

or 

> docker build -t fastapi:v1.0 .

#### Execute

> podman run -it -p 8000:8000 fastapi:v1.0

or

> docker run -it -p 8000:8000 fastapi:v1.0
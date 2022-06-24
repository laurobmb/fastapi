import subprocess
import sys
import os
import uvicorn

from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from subprocess import Popen

app=FastAPI()

path_to_output_file = '/tmp/index.html'
myoutput = open(path_to_output_file,'w')

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

ENVIROMENT_VERSION = os.getenv('ENVIROMENT')

class ModeloBase(BaseModel):
    usuario: str
    nome: str
    sobrenome: str
    cpf: int
    idade: int


class infos(BaseModel):
    date: str
    arquivos: str
    uptime: str
    hostname: str


def hostname():
    process = subprocess.run(['hostname'], 
        check=True, 
        stdout=subprocess.PIPE, 
        universal_newlines=True
    )
    output = process.stdout
    return output


def date():
    process = subprocess.run(['date'], 
        check=True, 
        stdout=subprocess.PIPE, 
        universal_newlines=True
    )
    output = process.stdout
    return output


def uptime():
    process = subprocess.run(['uptime'], 
        check=True, 
        stdout=subprocess.PIPE, 
        universal_newlines=True
    )
    output = process.stdout
    return output


def lss():
    process = subprocess.run(['ls','-lha'], 
        check=True, 
        stdout=subprocess.PIPE, 
        universal_newlines=True
    )
    output = process.stdout
    return output


def indexhtml():
    p = Popen(["ls","-lha"],
        stdout=myoutput,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    output, errors = p.communicate()
    output

    p = Popen(["date"],
        stdout=myoutput,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    output, errors = p.communicate()
    output
    
    p = Popen(["uptime"],
        stdout=myoutput,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    output, errors = p.communicate()
    output


@app.get("/")
async def returnindex():
    indexhtml()
    return FileResponse('pages/index.html')


@app.get("/json", response_model=ModeloBase)
async def modelo001():
    return ModeloBase(
        usuario = "laurobmb",
        nome = "Lauro",
        sobrenome = "Gomes",
        cpf = '321312321',
        idade = 37
    )


@app.get("/info", response_model=infos)
async def infos_web():
    return infos(
        date = date(),
        arquivos = lss(),
        uptime = uptime(),
        hostname = hostname()
    )


@app.get("/page")
async def returnindex():
    indexhtml()
    return FileResponse('pages/page1.html')


@app.get("/version")
async def read_root():
    version = f"{sys.version_info.major}.{sys.version_info.minor}"
    message = f"FastAPI rodando em Uvicorn. Usando Python de {ENVIROMENT_VERSION} {version}"
    return {"message": message}


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080)

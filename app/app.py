from fastapi import FastAPI, Request
from pydantic import BaseModel
import sys
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
import subprocess
from subprocess import Popen

path_to_output_file = '/tmp/index.html'
myoutput = open(path_to_output_file,'w+')

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
    
    p = Popen(["hostname"],
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


app=FastAPI()

class ModeloBase(BaseModel):
    usuario: str
    nome: str
    sobrenome: str
    cpf: int
    idade: int

@app.get("/", response_model=ModeloBase)
async def modelo001():
    return ModeloBase(
        usuario = "laurobmb",
        nome = "Lauro",
        sobrenome = "Gomes",
        cpf = '321312321',
        idade = 37
    )

@app.get("/date")
async def modelo002():
    cmd = subprocess.check_output("date")
    return cmd

@app.get("/info")
async def returnindex():
    indexhtml()
    return FileResponse('/tmp/index.html')

@app.get("/version")
async def read_root():
    version = f"{sys.version_info.major}.{sys.version_info.minor}"
    message = f"FastAPI rodando em Uvicorn. Usando Python {version}"
    return {"message": message}

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})

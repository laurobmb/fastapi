from fastapi import FastAPI
from pydantic import BaseModel
import sys

import subprocess
from subprocess import Popen

path_to_output_file = 'index.html'
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
    return FileResponse('index.html')


@app.get("/version")
async def read_root():
    version = f"{sys.version_info.major}.{sys.version_info.minor}"
    message = f"FastAPI rodando em Uvicorn. Usando Python {version}"
    return {"message": message}

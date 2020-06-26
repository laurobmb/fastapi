from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import sys

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
        cpf = '83789458934789573',
        idade = 37
    )

@app.get("/date")
async def modelo002():
    cmd = subprocess.check_output("date")
    return cmd

@app.get("/hostname")
async def modelo003():
    cmd = subprocess.check_output("hostname")
    return cmd    

@app.get("/version")
async def read_root():
    version = f"{sys.version_info.major}.{sys.version_info.minor}"
    message = f"FastAPI rodando em Uvicorn. Usando Python {version}"
    return {"message": message}

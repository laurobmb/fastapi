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
        cpf = '321312321',
        idade = 37
    )

@app.get("/date")
async def modelo002():
    cmd = subprocess.check_output("date")
    return cmd

@app.get("/info")
async def modelo003():
    DATE = subprocess.check_output(["date"], shell=True,universal_newlines=True)
    UPTIME = subprocess.check_output(["uptime"], shell=True,universal_newlines=True)
    HOSTNAME = subprocess.check_output(["hostname"], shell=True,universal_newlines=True)
    return DATE+UPTIME+HOSTNAME

@app.get("/version")
async def read_root():
    version = f"{sys.version_info.major}.{sys.version_info.minor}"
    message = f"FastAPI rodando em Uvicorn. Usando Python {version}"
    return {"message": message}

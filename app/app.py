import subprocess
import sys
import os
import uvicorn
import secrets

from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from subprocess import Popen
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials


ENVIROMENT_VERSION = os.getenv('ENVIROMENT')

app=FastAPI(
    title='Python FASTAPI deployment LAB',
    version=ENVIROMENT_VERSION+' 0.1.10',
    docs_url = None,
    redoc_url = None,
    contact={
        "name": "Lauro de Paula Gomes",
        "url": "https://laurobmb.wordpress.com/",
        "email": "laurobmb@gmail.com",
    }
)

security = HTTPBasic()

path_to_output_file = '/tmp/index.html'
myoutput = open(path_to_output_file,'w')

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


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
async def index():
    indexhtml()
    return FileResponse('pages/index.html')


@app.get("/json", response_model=ModeloBase)
async def ModeloBase():
    return ModeloBase(
        usuario = "laurobmb",
        nome = "Lauro",
        sobrenome = "Gomes",
        cpf = '321312321',
        idade = 37
    )


@app.get("/info", response_model=infos)
async def pod_infos():
    return infos(
        date = date(),
        arquivos = lss(),
        uptime = uptime(),
        hostname = hostname()
    )


@app.get("/page")
async def pagina():
    indexhtml()
    return FileResponse('pages/page1.html')


@app.get("/version")
async def version():
    version = f"{sys.version_info.major}.{sys.version_info.minor}"
    message = f'FastAPI rodando em Uvicorn. Python version: {version} Ambiente: {ENVIROMENT_VERSION}'
    return {"message": message}


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})

def checkFileSecret():
    import os.path
    secret_user_file="/opt/secrets/username" 
    secret_pass_file="/opt/secrets/password"
    secret_user_file_file_exists = os.path.exists(secret_user_file)
    secret_pass_file_file_exists = os.path.exists(secret_pass_file)

    if secret_user_file_file_exists:
        secret_user = open(secret_user_file,"r")
    else:
        secret_user = "error"

    if secret_pass_file_file_exists:
        secret_pass = open(secret_pass_file,"r")
    else:
        secret_pass = "error"

    return secret_user,secret_pass

    #configmap = open("/opt/config/page","r")

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    secret_user,secret_pass = checkFileSecret()
    correct_username = secrets.compare_digest(credentials.username, secret_user)
    correct_password = secrets.compare_digest(credentials.password, secret_pass)
    if not (correct_username and correct_password) or secret_user == 'error':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/users")
def read_current_user(username: str = Depends(get_current_username)):
    return {"username": username}

if __name__ == '__main__':
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8080,
        debug=False, 
        log_level="info")

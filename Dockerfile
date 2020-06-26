FROM centos/python-38-centos7
LABEL maintainer="Lauro Gomes <laurobmb@gmail.com>"
RUN pip install --upgrade pip
COPY app/ /app
WORKDIR /app
RUN python -m pip install -r requirements.txt 
EXPOSE 8000
#CMD [ "python -m uvicorn api:app" ] 
CMD [ "uvicorn", "--host", "0.0.0.0", "api:app", "--reload" ]

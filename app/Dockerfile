FROM centos/python-38-centos7:latest
LABEL maintainer="Lauro Gomes <laurobmb@gmail.com>"
RUN pip install --upgrade pip
COPY . /app
WORKDIR /app
RUN python -m pip install -r requirements.txt 
EXPOSE 8080
ENV ENVIROMENT=env
#CMD [ "python", "app.py" ]
CMD [ "uvicorn", "app:app", "--host","0.0.0.0","--port","8080","--log-level","info"]

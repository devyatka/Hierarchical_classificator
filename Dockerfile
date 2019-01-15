FROM python:2.7
MAINTAINER devyatka

RUN useradd -ms /bin/bash classifyer
WORKDIR /home/classifyer
COPY requirements.txt requirements.txt
COPY app app 
COPY flask flask
RUN pip install -r requirements.txt
RUN chmod +x app/__init__.py

ENV FLASK_APP app/__init__.py

RUN chown -R classifyer:classifyer ./
USER classifyer
EXPOSE 5000
ENTRYPOINT ["./app/__init__.py"]

FROM python:3.6.2

ENV DEPLOY_PATH /areyoufree_backend

RUN mkdir -p $DEPLOY_PATH
WORKDIR $DEPLOY_PATH

Add requirements.txt requirements.txt
RUN python3.6 -m pip install -r requirements.txt

Add . .

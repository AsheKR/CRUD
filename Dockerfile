FROM                        python:3.6.7-slim
MAINTAINER                  tech@ashe.kr

WORKDIR                     /srv

ADD                        ./app /srv/app/
ADD                        ./nginx /srv/nginx/
ADD                        ./gunicorn /srv/gunicorn/
ADD                        ./requirements /srv/requirements/

RUN                         pip install --upgrade pip
RUN                         pip install -r requirements/production.txt

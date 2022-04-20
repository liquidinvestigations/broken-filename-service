FROM python:3.9.1-buster

RUN mkdir /opt/app/
WORKDIR /opt/app/

ADD app.py runserver Pipfile Pipfile.lock  ./

RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile
RUN mkdir /data/

ENV FLASK_APP app.py
ENV FLASK_DEBUG 0
ENV DATA_LOCATION /data

EXPOSE 5000
CMD /opt/app/runserver

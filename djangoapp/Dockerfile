FROM python:3.6

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY Pipfile* /code/

RUN pip install pipenv && pipenv install --dev

COPY init /init/
COPY src /code/


RUN ["chmod", "+x", "/init/local_entrypoint.sh"]
ENTRYPOINT ["/init/local_entrypoint.sh"]

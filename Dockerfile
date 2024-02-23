FROM python:3.11-buster

RUN apt-get update && \
    apt-get install -y vim gettext

RUN apt-get clean all

RUN python3 -m pip install --upgrade pip

ENV AppHome=/usr/local/isudha/wikigpt

WORKDIR ${AppHome}

EXPOSE 80

COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt

ADD ./ ${AppHome}

RUN python3 manage.py collectstatic --noinput

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

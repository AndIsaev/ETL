FROM python:3.9.6-slim

RUN mkdir /code
WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements/base.txt /code
COPY requirements/production.txt /code

RUN python -m pip install --upgrade pip
RUN pip3 install -r /code/base.txt && pip3 install -r /code/production.txt
COPY ./entrypoint.sh .

COPY . .

ENTRYPOINT ["./entrypoint.sh"]
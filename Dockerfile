FROM python:3.9.6-slim

RUN mkdir /code
WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY movies_admin/requirements/base.txt /code
COPY movies_admin/requirements/production.txt /code

RUN python -m pip install --upgrade pip
RUN pip3 install -r /code/base.txt && pip3 install -r /code/production.txt
COPY movies_admin/entrypoint.sh .

COPY movies_admin .

ENTRYPOINT ["./entrypoint.sh"]
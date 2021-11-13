FROM python:3.9.6-slim
WORKDIR /code
COPY requirements.txt /code
RUN pip install -r /code/requirements.txt --no-cache-dir
COPY . /code
EXPOSE 8000
CMD python /code/load_data.py
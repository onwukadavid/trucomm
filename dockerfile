FROM python:3.11-slim

WORKDIR /trucomm/

COPY . /trucomm/

RUN apt-get update && apt-get install -y pkg-config python3-dev default-libmysqlclient-dev build-essential default-libmysqlclient-dev

RUN pip install -r requirements/dev.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
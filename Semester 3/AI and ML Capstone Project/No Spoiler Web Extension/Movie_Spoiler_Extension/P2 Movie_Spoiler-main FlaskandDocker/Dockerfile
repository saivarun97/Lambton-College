# syntax=docker/dockerfile:1

FROM python:3.10.2

WORKDIR /test-project

ADD . /test-project

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

#CMD ["python", "app.py"]
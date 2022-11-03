FROM python:latest AS base

FROM base as builder
RUN mkdir /install
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install --prefix=/install -r /requirements.txt

FROM base
RUN mkdir /project
ENV FLASK_APP api.py
WORKDIR /project
COPY --from=builder /install /usr/local
ADD . /project

ENTRYPOINT ["python", "-m", "flask", "run", "--host=0.0.0.0"]
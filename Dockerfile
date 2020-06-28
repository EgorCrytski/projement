FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY Pipfile* /code/

RUN pip install pipenv && \
    pipenv install --system --deploy --ignore-pipfile

COPY .. /code
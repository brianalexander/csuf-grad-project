FROM python:3.9-slim

RUN pip install --upgrade pip --user
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# https://github.com/psycopg/psycopg2/issues/684
# RUN apk update && apk add --no-cache postgresql-dev gcc python3-dev musl-dev

COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --system --deploy

COPY src/ .
ENTRYPOINT [ "python" ]
CMD [ "./intake_processed.py" ]

# https://stackoverflow.com/questions/55200135/python-docker-container-use-print
# https://stackoverflow.com/questions/11618898/pg-config-executable-not-found
# https://www.docker.com/blog/containerized-python-development-part-1/

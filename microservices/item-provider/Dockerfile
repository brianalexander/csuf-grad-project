FROM python:3.9-slim

RUN pip install --upgrade pip --user


WORKDIR /code

COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --system --deploy

COPY src/ .
ENV PYTHONUNBUFFERED=1
ENTRYPOINT [ "python" ]
CMD [ "./item_provider.py" ]

# https://stackoverflow.com/questions/55200135/python-docker-container-use-print
# https://stackoverflow.com/questions/11618898/pg-config-executable-not-found
# https://www.docker.com/blog/containerized-python-development-part-1/

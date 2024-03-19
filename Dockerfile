FROM python:3.9

ENV POETRY_VERSION=1.8.2
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache
ENV PYTHONUNBUFFERED 1

RUN python3 -m venv $POETRY_VENV \
	&& $POETRY_VENV/bin/pip install -U pip setuptools \
	&& $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

ENV PATH="${POETRY_VENV}/bin:${PATH}"

WORKDIR /app

COPY poetry.lock pyproject.toml /app
COPY . /app

RUN poetry install

COPY run.sh /app


FROM python:3.8.2

RUN apt-get update
RUN python -m pip install --no-cache-dir --upgrade poetry 

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY pyproject.toml poetry.lock ./ 
RUN poetry export -f requirements.txt --without-hashes -o /src/requirements.txt 

COPY ./requirements/requirements.txt /usr/src/app

#​ Install requirements 
COPY --from=requirements /src/requirements.txt . 
RUN pip install --no-cache-dir --user -r requirements.txt
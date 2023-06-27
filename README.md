[![Django CI](https://github.com/msm9401/apt-management-pilot/actions/workflows/django.yml/badge.svg)](https://github.com/msm9401/apt-management-pilot/actions/workflows/django.yml)
[![codecov](https://codecov.io/gh/msm9401/apt-management-pilot/branch/main/graph/badge.svg?token=TCA2B712HK)](https://codecov.io/gh/msm9401/apt-management-pilot)

# APT-Management-Backend

![erd](https://user-images.githubusercontent.com/70134073/229479827-e8fed654-9b76-408b-a4ec-a26432724ea3.png)

---

---

## 도커 개발 환경 실행 방법

<br>

1. repository를 다운받고 해당 위치로 이동 후 vscode열기

```
git clone https://github.com/msm9401/apt-management-pilot.git

cd apt-management-pilot

code .
```

<br>

2. repository의 최상단에 .env.dev 파일과 .env.postgres.dev 파일 추가하고 파일 내용을 아래와 같이 작성

```
# .env.dev 파일

DEBUG="1"

SECRET_KEY="django-insecure-&!0&y+zz$6w+i7m9+=0*h12af*gs^dkcr0xnjdomfio1lisd)c"
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1

SQL_ENGINE="django.db.backends.postgresql"
SQL_DATABASE="apt_management_db"
SQL_USER="apt_management_user"
SQL_PASSWORD="apt_management_password"
SQL_HOST="db"
SQL_PORT="5432"
```

```
# .env.postgres.dev 파일

POSTGRES_DB="apt_management_db"
POSTGRES_USER="apt_management_user"
POSTGRES_PASSWORD="apt_management_password"
```

<br>

3. 도커 실행

```
docker-compose up --build
```

❗️ 서버 작동 확인 : http://127.0.0.1:8000/admin 또는 http://localhost:8000/admin<br>
❗️ Mac에서 빌드 실패할 경우 베이스 이미지와 파이널 이미지의 FROM에 --platform=linux/amd64 추가 후 다시 실행.<br>

```
# Dockerfile

FROM --platform=linux/amd64 python:3.8.13-slim-buster as requirements

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && pip install --upgrade pip poetry

COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --without-hashes -o requirements-dev.txt --with dev

FROM --platform=linux/amd64 python:3.8.13-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY --from=requirements requirements-dev.txt /usr/src/app/
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements-dev.txt

COPY entrypoint.sh /usr/src/app/
RUN chmod +x /usr/src/app/entrypoint.sh

COPY . /usr/src/app/

ENTRYPOINT ["sh", "/usr/src/app/entrypoint.sh"]
```

<br>

4. 도커 컨테이너 진입 후 createsuperuser 실행

```
docker exec -it apt-management-pilot-web-1 /bin/bash

python manage.py createsuperuser
```

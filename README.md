[![Django CI](https://github.com/msm9401/apt-management-pilot/actions/workflows/django.yml/badge.svg)](https://github.com/msm9401/apt-management-pilot/actions/workflows/django.yml)
[![codecov](https://codecov.io/gh/msm9401/apt-management-pilot/branch/main/graph/badge.svg?token=TCA2B712HK)](https://codecov.io/gh/msm9401/apt-management-pilot)

# APT-Management-Backend

![erd](https://user-images.githubusercontent.com/70134073/229479827-e8fed654-9b76-408b-a4ec-a26432724ea3.png)

---

---

## 도커 개발 환경 실행 방법

1. repository를 다운받고 해당 위치로 이동 후 vscode열기

```
git clone https://github.com/msm9401/apt-management-pilot.git

cd apt-management-pilot

code .
```

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

3. 도커 실행

```
docker-compose up --build
```

4. 도커 컨테이너 진입 후 createsuperuser 실행

```
docker exec -it apt-management-pilot-web-1 /bin/bash

python manage.py createsuperuser
```

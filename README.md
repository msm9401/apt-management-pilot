[![Django CI](https://github.com/msm9401/apt-management-pilot/actions/workflows/django.yml/badge.svg)](https://github.com/msm9401/apt-management-pilot/actions/workflows/django.yml)
[![codecov](https://codecov.io/gh/msm9401/apt-management-pilot/branch/main/graph/badge.svg?token=TCA2B712HK)](https://codecov.io/gh/msm9401/apt-management-pilot)

# APT-Management-Backend

아파트 관리와 커뮤니티 기능을 제공하는 프로젝트

![erd](https://user-images.githubusercontent.com/70134073/229479827-e8fed654-9b76-408b-a4ec-a26432724ea3.png)

선배포 링크 : http://apt-management-bucket.s3-website.ap-northeast-2.amazonaws.com<br>
❗️ 배포 연습겸 프론트는 로그인과 회원가입만 일단 만들어서 배포(디자인 확정 X)<br>
❗️ 업데이트 버전 계속 배포 예정<br>

### 프로젝트 개요

- 각 아파트는 공지사항, 민원접수, 연락처, 주요 일정, 투표, 커뮤니티 기능을 이용할 수 있다.
- 해당 아파트 주민들은 회원가입 후 관리사무소에서 실제 주민인지 확인 후 각 아파트 페이지에 접근할 수 있다.
- 위의 기능을 이용함으로써 관리사무소는 아파트 관리를 조금 더 효율적으로 할 수 있고 주민 간에 소통이 강화되는 것을 기대할 수 있다.

### 프로젝트 간략 구성도

![구성도 drawio](https://github.com/msm9401/apt-management-pilot/assets/70134073/6042dcd5-09cb-4b36-8af6-f5377ce93393)

❗️ 배포 후 aws 콘솔에서 변경한 부분이 있어서 깃허브 코드랑 다른 부분이 있을 수 있습니다.<br>
❗️ 그림상에는 없지만 redis컨테이너도 ec2에서 돌아가고 있습니다.<br>
❗️ gunicorn은 django컨테이너 안에 있습니다.<br>

### 문제 상황 & 해결 & 회고 등등 기록

<details>
<summary> 개발 초기 단계 부터 성능(퍼포먼스)에 대해 고민할 것인가?</summary><br>
<div markdown="1">
 결론부터 말하면 "상황판단을 잘하자" 이다. 우선 나는 성능(퍼포먼스)이 굉장히 중요하다고 생각한다. 유저는 필요에 의해 내 서비스를 이용하기 위해서 들어왔고 어떻게든 좋은 이미지를 심어주어서 다음에도 이용하게 만들기 위해서는 처음에 받는 느낌, 즉 첫인상이 그 서비스를 계속적으로 이용하는 데 있어서 가장 큰 요인 중에 하나라고 생각한다. 하지만 너무 개발 초기 단계부터 성능(퍼포먼스)에 신경을 쓰게 되면 개발 진척도가 너무 느려지는 것을 느꼈다. 이미 어느 정도 유저풀이 확보되어 있는 기업에서 새로운 기능을 도입하는 데에는 성능을 어느 정도 신경 쓰면서 개발하는 것이 도움이 되겠지만 나 같은 경우는 혼자 하는 개인 프로젝트이고 기능들을 빨리 개발하고 서비스해 보면서 차차 성능을 개선하는 것이 훨씬 좋은 판단이었을 것이다. 아마 하루하루가 생존인 스타트업일 경우도 빠르게 일단 새로운 기능을 도입하는 게 맞는 상황 판단일지도 모른다. 물론 어떤 프로젝트냐에 따라 다를 수도 있다. 결국 내가 마주하고 있는 상황에 따라 우선순위를 잘 따져가면서 프로젝트 진행을 해야 한다고 느꼈다.<br><br>
  
- **성능(퍼포먼스)를 위해 어떤 고민?**
    - 서버 확장, 로드 밸런싱, CDN 사용과 같이 클라우드 서비스로 바로 이용할 수 있는 부분 말고 기본적인 코드나 db 최적화에 대해 고민
    - 기본적으로 debug-toolbar를 참고하여 한 번에 불러올 수 있는 정보들은 조인을 이용하거나 IN 명령어로 쿼리 수를 줄여줌
    - filter 조건에 자주 사용되는 아파트 이름에 인덱스 적용
    - redis를 이용하여 반복적인 요청을 처리하는데 필요한 리소스들을 줄임<br><br>

- **성능(퍼포먼스) 테스트 시나리오 & 결과?**

  - 가장 많이 이용이 예상되는 피드 서비스로 진행
  - 시나리오로는 로그인하고 피드 리스트 및 개별 피드 접근 그리고 피드 작성으로 진행
  - 일반적으로 read 요청이 많을 거라고 예상하고 피드 리스트 접근에 가장 많은 부하를 줌
  - 유저 약 100명 기준 Response times가 7500ms에서 1600ms로 개선
  - 항상 유저가 약 100명부터 그래프가 확 꺾이기 시작하고 rps가 갑자기 0으로 되는 현상이 있었는데 max_connections 설정이 100으로 설정되어 있어서 늘려주었음<br><br>

- **한계점 & 개선해야 할 점 & 계획?**
  - 로컬 테스트 환경이라 실 서비스와는 괴리가 큼
  - 아직 모니터링 환경을 구축하지 않았음
  - 모니터링 환경을 구축해서 그래프 꺾이는 지점에서의 cpu, 메모리 등 리소스 사용률을 확인 후 서버를 늘려주던지 DBCP의 connection 상태를 확인해서 django와 postgresql의 connection 설정값을 바꿔주던지 결정할 수 있음
  - redis를 브로커로 이용해서 celery와 함께 작업을 비동기적으로 처리<br><br>

❗️ 혼자 독학으로 진행하는 프로젝트라 잘못된 내용이 있을 수 있습니다.<br>

  </div>
  </details>

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
❗️ Mac에서 빌드 실패할 경우 아래와 같이 베이스 이미지와 파이널 이미지의 FROM에 --platform=linux/amd64 추가 후 다시 실행.<br>
❗️ 국토교통부에서 제공되는 api가 종종 튕기는 경우가 있음.<br>

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

---

---

## API 문서

❗️ 지속 업데이트 중

https://documenter.getpostman.com/view/25021212/2s93zCa1w2

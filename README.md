[![Django CI](https://github.com/msm9401/apt-management-pilot/actions/workflows/django.yml/badge.svg)](https://github.com/msm9401/apt-management-pilot/actions/workflows/django.yml)
[![codecov](https://codecov.io/gh/msm9401/apt-management-pilot/branch/main/graph/badge.svg?token=TCA2B712HK)](https://codecov.io/gh/msm9401/apt-management-pilot)

# APT-Management-Backend

아파트 관리와 커뮤니티 기능을 제공하는 프로젝트

![erd](https://user-images.githubusercontent.com/70134073/229479827-e8fed654-9b76-408b-a4ec-a26432724ea3.png)
❗️ 개발과정 중 변경될 수도 있습니다. (변경사항이 있다면 개발 완료 후 최종본 업데이트 예정)<br>

선배포 링크 : http://apt-management-bucket.s3-website.ap-northeast-2.amazonaws.com<br>
❗️ 기능 확인 목적의 데모 사이트<br>
❗️ 업데이트 버전 계속 배포 예정<br><br>
❗️ 아래와 같은 화면을 확인하시려면 회원가입 후 검색 창에 "용인신갈푸르지오" 를 검색 후 초록색 하트를 눌러 본인 아파트로 등록 후(현재는 별도 인증 과정 없음) 확인해 주세요.<br>

<center><img src="https://github.com/msm9401/apt-management-pilot/assets/70134073/dcc68445-cf9f-4ebe-9137-cb170386878e" width="400" height="250"/></center>

<center><img src="https://github.com/msm9401/apt-management-pilot/assets/70134073/b0d2426f-fe8f-4be5-b5a4-226f8b66491c" width="400" height="250"/></center>

<center><img src="https://github.com/msm9401/apt-management-pilot/assets/70134073/e2cde4a3-5d03-4067-9373-676216a2902f" width="400" height="250"/></center>

<center><img src="https://github.com/msm9401/apt-management-pilot/assets/70134073/8e7189b2-cb99-4e1a-acdd-45ef7397a73a" width="400" height="250"/></center>

### 프로젝트 개요

- 각 아파트는 공지사항, 민원접수, 연락처, 주요 일정, 투표, 커뮤니티 기능을 이용할 수 있다.
- 해당 아파트 주민들은 회원가입 후 관리사무소에서 실제 주민인지 확인 후 각 아파트 페이지에 접근할 수 있다.
- 위의 기능을 이용함으로써 관리사무소는 아파트 관리를 조금 더 효율적으로 할 수 있고 주민 간에 소통이 강화되는 것을 기대할 수 있다.

### 프로젝트 배포 환경 구성도

![KakaoTalk_20231119_224816524](https://github.com/msm9401/apt-management-pilot/assets/70134073/a77d38bf-38ca-497e-9cad-5485909d67ac)

❗️ 배포 후 aws 콘솔에서 변경한 부분이 있어서 깃허브 코드랑 다른 부분이 있을 수 있습니다.<br>

### 프로젝트 도커 개발 환경 구성도

![KakaoTalk_20231119_224816664](https://github.com/msm9401/apt-management-pilot/assets/70134073/3f9b40ed-be19-458b-86c5-2358117f164c)

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
<details>
  <summary> Index를 이용해서 쿼리 속도 개선하기</summary><br>
<div markdown="1">
pagination을 적용하면서 유난히 오래 걸리는 쿼리문이 발생하였다.<br><br>

![SmartSelectImage_2023-09-10-23-47-51](https://github.com/msm9401/apt-management-pilot/assets/70134073/02c409a0-d0dd-4839-babf-ca23e0593a3f)

![SmartSelectImage_2023-09-10-23-49-40](https://github.com/msm9401/apt-management-pilot/assets/70134073/55453370-e413-4fba-9402-5aac7df77544)

확인해 보니 apartment 테이블을 full scan하면서 count(개수)를 구하는 쿼리문.<br>
현재 apartment 테이블에 존재하는 Index는 kapt_name(단지 이름)에 대한 Index밖에 없었기 때문에 kapt_code(단지 코드)에 대한 인덱스를 추가하기로 결정.<br>

![SmartSelectImage_2023-09-13-01-12-07](https://github.com/msm9401/apt-management-pilot/assets/70134073/8296dfde-dd68-4692-8bbf-43934fa2c10a)

![SmartSelectImage_2023-09-13-01-12-32](https://github.com/msm9401/apt-management-pilot/assets/70134073/251136b0-4bab-4cd0-8042-819cd199ce75)

결과 : 115.99ms --> 2.20ms<br><br>
kapt_code(단지 코드)에 대한 Index를 추가한 결과 covering Index 처리되면서 쿼리 속도가 대폭 개선됨을 확인할 수 있었다.

</div>
</details>

<details>
  <summary> 캐싱 전략을 정교하게 수립하지 못해서 겪은 문제점</summary><br>
<div markdown="1">
우선 내가 데이터를 읽을 때 취했던 전략은 캐시에 저장된 데이터가 있는지 우선적으로 확인하는 전략이었다.
만일 캐시에 데이터가 없으면 DB에서 조회하고 redis에 업데이트하는 방식이었다.
이 방식을 택했던 이유는 원하는 데이터만 별도로 캐시에 저장(쿼리 캐시) 하고 redis에 문제가 생기더라도 DB에서 데이터를 가져올 수 있기 때문에 서비스를 이용하는 데에는 문제가 없다고 판단됐기 때문이다. <br><br>
이 방식에서 고려해야 할 점은 캐시 된 데이터와 DB의 데이터가 같은 데이터임에도 불구하고 정보값이 서로 다른 현상이다. 이 문제가 있음을 사전에 인지하고 있었기 때문에 나름 데이터에 Write 요청이 오고 나서 캐시값을 삭제해 주거나 ttl 설정을 하는 대비를 했었는데 이게 생각보다 많이 정교해야 했다. 화면에 정보를 띄우는데 하나의 테이블에서 모든 정보를 보여주면 좋겠지만 현실은 그렇지 않다. 여러 테이블에서 정보들을 가져온다. 그래서 미쳐 생각하지 못한 부분에서 캐시 정보를 업데이트하지 못하고 실제 DB와 다른 데이터를 보여주는 경우가 생긴다. 나 같은 경우는 피드 부분에서만 캐시 정보를 처리하다가 댓글을 수정해도 피드에서 보여주는 댓글은 수정 전 정보를 그대로 보여줘서 ttl이 지나야 정보가 업데이트되곤 했었고 홈 화면에서 유저의 아파트 정보를 보여주는 부분에서 유저가 아파트 등록을 하고 나서는 홈 화면에 등록된 유저의 아파트 정보를 띄워줘야 하는데 빈 화면을 보여주어서 서비스 진행 자체를 못하게 되는 치명적인 문제도 있었다. <br><br>
결국 피드에서의 캐시는 일단 전부 걷어내고 홈 화면에서의 캐시만 남겨두었다. ( 아파트 검색 결과에 캐시 적용 예정 ) 댓글 정보 변경 시에도 캐시를 업데이트하고 해도 되지만
댓글 특성상 자주 변경될 가능성이 높이 때문에 캐시를 이용하는데 부적절하다는 생각이 들었다. 아니면 redis에 먼저 저장하고 db에 저장하는 방식을 택해서 항상 최신 데이터를 유지해도 됐겠지만 항상 2단계를 거치면서 성능을 다운시키고 싶지는 않았다. 왜냐하면 캐시를 구성하는 목적은 빠른 성능 확보가 가장 큰 이유라고 생각하기 때문이다.

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

3. 로깅 설정 이름 변경 및 캐시 설정 주석 처리 해제

```
# repository의 최상단에 logs폴더 만들기

# log 관련 파일들은 .gitignore에서 제외처리돼서 직접 만들어줘야 함

mkdir logs
```

```
# config/settings/develop.py

# 로깅 설정 부분 DEV_LOGGING 에서 LOGGING 으로 이름 변경
DEV_LOGGING = {
    "version": 1,
    ...
}
```

```
# config/settings/base.py

# 캐시 설정 주석 처리된 부분 해제
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         ...
#     }
# }
```

❗️ 위 3번 설정들은 안해도 도커 실행은 되지만 실행되는 컨테이너들을 전부 활용하려면 설정 필요.<br>

<br>

4. 도커 실행

```
docker-compose up --build
```

❗️ 서버 작동 확인 : http://127.0.0.1:8000/admin 또는 http://localhost:8000/admin<br>
❗️ 프로메테우스 작동 확인 : http://127.0.0.1:9090<br>
❗️ 그라파나 작동 확인 : http://127.0.0.1:3000 아이디 : admin, 패스워드 : admin<br>connections 탭에서 새로운 데이터 소스 추가할 필요 없이 explore 탭에 들어가서 Loki와 Prometheus 바로 조회 가능
<br><br>
❗️ Mac에서 빌드 실패할 경우 아래와 같이 각 FROM에 `--platform=linux/amd64` 추가 후 다시 실행. Dockerfile을 아래 파일로 변경 후 빌드. (필자는 WSL2 환경)<br>

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

4. 장고 컨테이너 진입 후 데이터 세팅 및 admin생성

```
# 컨테이너 진입
docker exec -it django /bin/bash

# admin 생성 (아이디와 비밀번호만 필수)
python manage.py createsuperuser

# 아파트 데이터 세팅
python manage.py get_houses
```

❗️ 컨테이너 진입 안될 경우 `docker ps` 로 8000번 포트 컨테이너 이름 확인 후 진입.<br>
❗️ 국토교통부에서 제공되는 api가 종종 튕기는 경우가 있음. 튕기더라도 재시도. 여러 번 재시도해도 튕길경우 점검중일 가능성 큼.<br>

---

---

## API 문서

❗️ 지속 업데이트 중

https://documenter.getpostman.com/view/25021212/2s93zCa1w2

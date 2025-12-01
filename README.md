# BGround Homepage

BGround 회사의 홈페이지 프로젝트입니다. HTML/CSS 프론트엔드, FastAPI 백엔드, PostgreSQL 데이터베이스로 구성되어 있습니다.

## 프로젝트 구조

```
homepage/
├── front-end/          # HTML/CSS/JS 프론트엔드
├── back-end/           # FastAPI 백엔드
├── docker-compose.yml  # Docker Compose 설정
└── README.md
```

## 기술 스택

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **Session Store**: Redis
- **Container**: Docker & Docker Compose
- **Web Server**: Nginx (URL 리라이팅)

## 기능

- 회사 소개 페이지
- 제품 소개 페이지
- 문의하기 폼 (데이터베이스 저장)
- 관리자 페이지 (문의 데이터 조회)
- Redis 기반 세션 관리
- 사용자 인증 및 권한 관리
- 깔끔한 URL 구조 (파일명 숨김)

## URL 구조

Nginx 설정을 통해 파일명이 URL에 표시되지 않는 깔끔한 URL 구조를 제공합니다:

- **홈페이지**: `/` (index.html)
- **회사소개**: `/company` (company01.html)
- **Our Story**: `/company/story` (company02.html)
- **Our Team**: `/company/team` (company03.html)
- **제품소개**: `/products` (products.html)
- **문의하기**: `/contact` (contactus.html)
- **관리자 페이지**: `/-_-/admin` (admin.html)

## 실행 방법

### 1. Docker Compose로 전체 스택 실행

```bash
# 프로젝트 루트 디렉토리에서 실행
docker-compose up -d
```

### 2. 개별 서비스 확인

```bash
# 컨테이너 상태 확인
docker-compose ps

# 로그 확인
docker-compose logs -f [service_name]
```

### 3. 접속 정보

- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000
- **Admin Page**: http://localhost/-_-/admin
- **Database**: localhost:5432
- **Redis**: localhost:6379

### 4. API 엔드포인트

#### 공개 API
- `GET /`: API 상태 확인
- `POST /api/contactus`: 문의하기 데이터 저장

#### 인증 필요 API
- `POST /api/login`: 사용자 로그인
- `POST /api/logout`: 사용자 로그아웃
- `GET /api/session`: 현재 세션 정보 조회
- `POST /api/session/extend`: 세션 만료 시간 연장
- `GET /api/contactus`: 모든 문의하기 데이터 조회 (인증 필요)
- `GET /api/contactus/{id}`: 특정 문의하기 데이터 조회 (인증 필요)

#### 기본 로그인 정보
- **Username**: admin
- **Password**: admin123

## 문의하기 폼 필드

- `name`: 이름 또는 기업명 (필수)
- `mail`: 이메일 (필수)
- `telno`: 전화번호 (선택)
- `referrer`: 방문 경로 (선택)
- `title`: 제목 (필수)
- `contents`: 내용 (필수)
- `confirm`: 개인정보 수집 동의 (필수)

## 데이터베이스 조회 방법

### 1. 관리자 페이지 사용
- http://localhost/-_-/admin 접속
- 실시간으로 문의 데이터 확인 가능
- 통계 정보 제공 (총 문의 수, 오늘 문의 수, 동의 완료 수)

### 2. API 직접 호출
```bash
# 모든 문의 조회
curl http://localhost:8000/api/contactus

# 특정 문의 조회 (ID: 1)
curl http://localhost:8000/api/contactus/1
```

### 3. 데이터베이스 직접 접속
```bash
# PostgreSQL 컨테이너에 접속
docker-compose exec postgres psql -U homepage_user -d homepage_db

# 문의 데이터 조회
SELECT * FROM contactus ORDER BY created_at DESC;
```

## 개발 환경 설정

### 로컬 개발

1. **PostgreSQL 설치 및 설정**
```bash
# PostgreSQL 설치 (Ubuntu)
sudo apt-get install postgresql postgresql-contrib

# 데이터베이스 생성
sudo -u postgres createdb homepage_db
sudo -u postgres createuser homepage_user
sudo -u postgres psql -c "ALTER USER homepage_user WITH PASSWORD 'homepage_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE homepage_db TO homepage_user;"
```

2. **백엔드 실행**
```bash
cd back-end
pip install -r requirements.txt
uvicorn main:app --reload
```

3. **프론트엔드 실행**
```bash
cd front-end
# 간단한 HTTP 서버 실행
python -m http.server 8080
```

## Redis 세션 관리

이 프로젝트는 Redis를 사용하여 사용자 세션을 관리합니다.

### 세션 관리 기능

- **세션 생성**: 사용자 로그인 시 Redis에 세션 데이터 저장
- **세션 조회**: 쿠키 기반 세션 토큰으로 사용자 정보 조회
- **세션 연장**: 자동 세션 만료 시간 연장
- **세션 삭제**: 로그아웃 시 세션 데이터 삭제
- **보안**: 세션 토큰 암호화 및 HttpOnly 쿠키 사용

### 세션 설정

- **세션 만료 시간**: 1시간 (3600초)
- **세션 저장소**: Redis
- **세션 토큰**: 암호화된 쿠키 기반

### 테스트 방법

```bash
# 세션 관리 기능 테스트
python test_session.py
```

## 데이터베이스 스키마

```sql
CREATE TABLE contactus (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    mail VARCHAR(100),
    telno VARCHAR(50),
    referrer VARCHAR(100),
    title VARCHAR(200),
    contents TEXT,
    confirm BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 문제 해결

### 포트 충돌
- 80번 포트가 사용 중인 경우: `docker-compose.yml`에서 포트 변경
- 8000번 포트가 사용 중인 경우: `docker-compose.yml`에서 포트 변경

### 데이터베이스 연결 오류
```bash
# PostgreSQL 컨테이너 재시작
docker-compose restart postgres

# 데이터베이스 로그 확인
docker-compose logs postgres
```

### CORS 오류
- 백엔드의 CORS 설정 확인
- 프론트엔드에서 올바른 API URL 사용 확인

### 관리자 페이지 접속 불가
- 프론트엔드 컨테이너가 정상 실행 중인지 확인
- 브라우저에서 http://localhost/-_-/admin 직접 접속 시도

### URL 리라이팅 문제
- Nginx 설정 파일 확인: `front-end/nginx.conf`
- 컨테이너 재빌드: `docker-compose build frontend`
- 컨테이너 재시작: `docker-compose restart frontend`

## 배포

프로덕션 환경에서는 다음 사항을 고려하세요:

1. 환경 변수 설정
2. 보안 강화 (CORS 설정, 데이터베이스 비밀번호 등)
3. SSL/TLS 인증서 설정
4. 로그 관리
5. 백업 전략
6. 관리자 페이지 접근 제한

## 라이선스

Copyright © BGround 
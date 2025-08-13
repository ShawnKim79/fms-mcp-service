# FMS-MCP-Study

AI 챗봇을 통해 주민과 자원봉사 운전자를 연결하는 마을 라이드 셰어링 모노레포입니다. 백엔드(FastAPI), 슬랙 봇 API, 그리고 에이전트(MCP) 실험 코드를 포함합니다.

## 프로젝트 개요
- **비전:** "AI 기술로 이웃을 연결하여, 누구나 소외되지 않는 따뜻한 이동 경험 제공"
- **핵심 컨셉:** 복잡한 앱 설치 없이, 문자/카카오톡 등 익숙한 채팅으로 차량을 요청하고 도움을 받는 서비스

## 주요 사용자
- **탑승객(주민):** 스마트폰 앱 사용이 익숙하지 않아도 채팅으로 쉽게 이동 지원을 요청
- **자원봉사 운전자:** 가능한 시간에 맞춰 이웃의 이동을 돕고 활동을 관리
- **AI 챗봇:** 자연어 메시지를 이해해 적절한 안내와 연결(추후 MCP 에이전트로 확대)

## 배경
이 프로젝트는 상업적 이익을 추구하지 않고, AI 기술을 통해 이웃 간 나눔을 활성화하여 지역 주민의 이동권을 보장하는 것을 목표로 합니다. 스마트폰 앱 설치 없이도 문자·카카오톡·Slack 같은 익숙한 채팅 환경에서 차량 요청과 매칭이 가능하도록 설계되었습니다.

## 컴포넌트 역할과 상호작용
- **`chatbot`**: Slack 이벤트(`/slack/events`)를 수신하고 기본 명령을 처리하거나 메시지를 MCP로 중계합니다.
- **`mcp_server`**: 사용자 의도를 해석하는 에이전트 실험 코드가 포함됩니다. 의도에 따라 FMS API 호출을 수행하도록 확장 가능합니다. (실험적)
- **`fms_server`**: 운행 경로/승객/탑승 요청 도메인에 대한 REST API를 제공합니다. 기본 포트는 8001입니다.

상호작용 흐름 예시
1. 사용자가 Slack 채널에 메시지를 입력
2. `chatbot`이 이벤트를 수신해 기본 명령은 자체 처리, 그 외는 `mcp_server`로 전달
3. `mcp_server` 에이전트가 의도를 파악하고 필요한 경우 `fms_server` API를 호출
4. 처리 결과를 사용자에게 메시지로 회신

## 기능 개요
- **자연어 처리 기반 상호작용:** 사용자의 자연어 요청을 분석해 필요한 정보를 추출하고 안내(에이전트 실험 코드 포함)
- **운행 경로 관리:** 출발/도착지, 출발 시각을 가진 경로 등록 및 조회
- **승객 관리:** 주민 기본 정보 등록과 조회
- **Slack 연동:** 워크스페이스 이벤트 수신, 기본 명령 처리, 에이전트로 메시지 중계

참고: 고도화 기능(예약/취소, 운전자 스케줄 관리 등)은 PRD에 기술되어 있으나 현재 레포 내 구현은 진행 중입니다.

## 레포 구성
- `fms_server/`: FastAPI 기반 FMS(운행 경로, 승객, 탑승 요청 등) 백엔드. 기본 포트 8001
- `chatbot/`: Slack 이벤트 수신 및 MCP 연계용 FastAPI 앱. 기본 포트 5000
- `mcp_server/`: 에이전트/도구 샘플(실험적)

## 빠른 시작
### 사전 준비
- Python 3.11
- PostgreSQL 14+
- (선택) Slack 워크스페이스와 봇 토큰/서명 시크릿

### 1) 데이터베이스 준비 (PostgreSQL)
아래 예시로 계정/DB를 만듭니다.
```sql
CREATE USER fms_user PASSWORD 'fms_password';
CREATE DATABASE fms OWNER fms_user;
```

환경변수(기본값 있음)를 필요시 설정합니다.
```bash
export DB_HOST=localhost
export DB_PORT=5432
export DB_USER=fms_user
export DB_PASSWORD=fms_password
export DB_NAME=fms
```

### 2) FMS 서버 실행 (`fms_server`)
필요 패키지 설치 후 서버를 실행합니다.
```bash
python -m pip install --upgrade pip
python -m pip install fastapi uvicorn sqlalchemy psycopg2-binary passlib pydantic
python fms_server/app/main.py
# 또는
uvicorn fms_server.app.main:app --host 0.0.0.0 --port 8001 --reload
```
기본 주소: `http://localhost:8001`

### 3) Slack 챗봇 실행 (`chatbot`)
환경 파일을 준비하고 의존성을 설치합니다.
```bash
cp chatbot/.env.example chatbot/.env
# .env에 SLACK_BOT_TOKEN, SLACK_SIGNING_SECRET, MCP_API_URL, MCP_API_KEY 값을 채워주세요.

python -m pip install -r chatbot/requirements.txt
python chatbot/app/main.py
# 또는
uvicorn chatbot.app.main:app --host 0.0.0.0 --port 5000 --reload
```
기본 주소: `http://localhost:5000`

Slack 이벤트 요청 URL은 예: `http://<공개 URL>/slack/events` (로컬은 ngrok 등으로 터널링)

## 환경 변수
### 공통/FMS
- `DB_HOST`(기본 `localhost`)
- `DB_PORT`(기본 `5432`)
- `DB_USER`(기본 `fms_user`)
- `DB_PASSWORD`(기본 `fms_password`)
- `DB_NAME`(기본 `fms`)

### Chatbot (`chatbot/.env` 사용)
- `SLACK_BOT_TOKEN`
- `SLACK_SIGNING_SECRET`
- `MCP_API_URL`(예: `http://localhost:8000`)
- `MCP_API_KEY`
- `LOG_LEVEL`(기본 `INFO`)

## API 빠른 참고 (FMS)
기본 URL: `http://localhost:8001`

- 경로: `GET /fms/routes`
  - 쿼리: `start_time`(ISO8601), `end_time`, `departure_location_name`, `destination_location_name`
- 경로 생성: `POST /fms/routes`
  - 바디 예:
    ```json
    {
      "driver_id": null,
      "car_plate_number": null,
      "departure_location_name": "보건소",
      "departure_time": "2025-08-13T09:00:00",
      "destination_location_name": "읍사무소"
    }
    ```
- 승객 생성: `POST /fms/passenger/`
  - 바디 예:
    ```json
    {
      "password": "secret",
      "name": "홍길동",
      "nickname": "길동",
      "contact_info": "010-1234-5678"
    }
    ```
- 승객 조회: `GET /fms/passenger/{passenger_id}`

예시 cURL
```bash
# 경로 생성
curl -X POST http://localhost:8001/fms/routes \
  -H "Content-Type: application/json" \
  -d '{
    "departure_location_name":"보건소",
    "departure_time":"2025-08-13T09:00:00",
    "destination_location_name":"읍사무소"
  }'

# 경로 검색
curl "http://localhost:8001/fms/routes?departure_location_name=%EB%B3%B4%EA%B1%B4%EC%86%8C&destination_location_name=%EC%9D%8D%EC%82%AC%EB%AC%B4%EC%86%8C"
```

참고: 일부 테스트/문서에 `ride_routes`로 표기된 곳이 있으나 현재 컨트롤러 경로는 `routes`입니다.

## 현황 및 주의사항
- `mcp_server`는 에이전트/도구 통합 실험 코드로, 실제 배포/보안 구성은 별도 작업이 필요합니다.
- FMS의 `Trip` 관련 기능은 서비스 레이어에 존재하나 공개 라우터가 아직 제공되지 않습니다. 공개 엔드포인트는 본 문서의 API 섹션을 따르세요.
- 기존 문서(PRD/README)의 일부 항목은 방향성을 설명하며, 현재 코드와 차이가 있을 수 있습니다.

## 테스트와 디버깅
- FMS 테스트: `tox -e py311` (디렉토리: `fms_server/`)
  - `tox.ini`는 `pytest`, `fastapi`, `uvicorn`, `sqlalchemy`, `psycopg2-binary`, `httpx` 등을 설치합니다.
- VS Code 디버깅: `.vscode/launch.json`에 `fms_server/app/main.py` 실행 설정 제공

## 트러블슈팅
- DB 연결 오류: `DB_HOST/PORT/USER/PASSWORD/NAME` 환경변수를 확인하고 DB가 기동 중인지 확인하세요.
- psycopg2 설치 실패: `python3-dev`, `libpq-dev` 등 빌드 도구가 필요할 수 있습니다. WSL에서 `sudo apt install build-essential libpq-dev python3-dev` 후 재시도하세요.
- Slack 401/403: 토큰/서명 시크릿이 올바른지, 이벤트 구독 URL이 공개 접근 가능한지 확인하세요.

## 라이선스
- 라이선스: `LICENSE.md` 참조

## 참고 문서
- `fms_server/README.md`: DB/테이블 예시 스키마
- 각 `prd.md`: 배경과 기능 개요

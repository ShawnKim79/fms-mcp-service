# FMS Server Documentation

## 1. 개요 (Overview)
- **프로젝트 목적**: 차량 관리 시스템(FMS)의 백엔드 API 서버.
- **주요 기능**: 승객, 운행 경로, 여정(탑승) 정보 관리 및 인증.

## 2. 기술 스택 (Tech Stack)
- **Web Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **DB Migration**: Alembic
- **Testing**: Pytest, Tox
- **Authentication**: JWT (JSON Web Token)

## 3. 아키텍처 (Architecture)
- **패턴**: 계층형 아키텍처 (Layered Architecture)
- **`controllers`**: API 엔드포인트 정의 (HTTP 요청/응답 처리)
- **`services`**: 핵심 비즈니스 로직 구현
- **`models`**: 데이터베이스 테이블 스키마 (SQLAlchemy models)
- **`domains`**: 비즈니스 도메인 객체 (Pydantic models)
- **`config`**: 데이터베이스 연결 등 설정 관리

## 4. 데이터베이스 스키마 (Database Schema)
- **`PassengerDB`**: 승객 정보
- **`RouteDB`**: 차량 운행 경로 정보
- **`TripDB`**: 승객의 여정(탑승) 정보

## 5. 주요 API 엔드포인트 (API Endpoints)
- `POST /fms/auth/token`: 로그인 및 토큰 발급
- `POST /fms/passengers`: 신규 승객 생성
- `POST /fms/routes`: 신규 운행 경로 생성

## 6. 실행 및 테스트 방법 (How to Run & Test)
- **서버 실행**: fms_server 디렉토리에서 `python .\fms_server\app\main.py`를 실행한다. 현재 모든 패키지 네임스페이스 구조가 이에 맞춰져 있음에 주의할것.
- **테스트 실행**: `tox` 또는 `pytest tests/`

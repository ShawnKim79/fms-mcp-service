
## 제품 요구사항 정의서 (PRD) - 마을 기반 카셰어링 서비스 RestAPI 서버

### 1. 개요

이 문서는 작은 마을을 위한 **무료 카셰어링 서비스**의 RestAPI 서버 구축에 필요한 요구사항을 정의합니다. 본 서비스는 운전자가 마을 외부로 이동하거나 진입할 때 **아이들을 승객으로 안전하게 태울 수 있도록** 지원하며, 운전자와 승객 간의 효율적인 매칭 및 정보 관리를 목표로 합니다. 서버는 운행 경로, 승객, 탑승 요청 정보를 관리하고, LLM 기반 봇과의 연동을 통해 사용자 편의성을 극대화합니다.

### 2. 목표

- **주요 목표:** 마을 주민들의 이동 편의성을 높이고, 특히 아이들의 안전하고 효율적인 통학/이동을 돕는 커뮤니티 기반 무료 카셰어링 서비스 제공.
- **세부 목표:**
    - 운전자와 승객(아이들) 간의 매칭을 위한 직관적인 운행 및 탑승 정보 관리.
    - LLM 기반 봇과의 원활한 통신을 통한 정보 등록, 조회, 요청 기능 구현.
    - 안정적인 RestAPI를 통해 웹/모바일 클라이언트 및 봇과의 연동 지원.

### 3. 대상 사용자

- **운전자:** 차량을 소유하고 있으며, 마을 외부 이동 시 아이들을 태울 의향이 있는 마을 주민.
- **승객 (아이들의 보호자):** 아이들의 안전한 이동을 위해 차량 탑승을 원하는 마을 주민.
- **LLM 기반 봇:** 운전자 및 승객과의 채팅 인터페이스를 통해 서비스와 연동되는 봇.
- **서비스 운영자:** 서비스 전반의 관리 및 모니터링을 담당하는 운영팀.

### 4. 서버 동작 환경

- **기반 기술:** Python + FastAPI
- **통신 방식:** RestAPI (HTTP 요청/응답)
- **봇 통신:** LLM 기반 봇과 MCP (Message Communication Protocol)를 통해 운행 정보 등록, 조회, 탑승 요청 등 상호작용.
- **데이터베이스:** PostgreSQL

### 5. 서비스 기초 정보

본 서비스에서 관리할 핵심 데이터 구조는 다음과 같습니다. 각 섹션에는 해당 정보를 생성하거나 조회할 때 사용될 JSON 데이터 샘플이 포함됩니다.

#### 5.1. 승객 정보 (Passenger)

- **이름 (name):** `string`, 필수
- **연락처 (contact_info):** `string`, 필수 (전화번호 또는 기타 연락 수단)
- **ID (id):** `UUID`, 서버에서 자동 생성

**JSON 데이터 샘플:**

**등록 요청:**

JSON

```
{
  "name": "김영희",
  "contact_info": "010-1234-5678"
}
```

**등록 응답/조회:**

JSON

```
{
  "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "name": "김영희",
  "contact_info": "010-1234-5678"
}
```

#### 5.2. 운행 경로 정보 (Ride Route)

- **운전자 정보 (driver_id):** `UUID`, 필수 (등록된 운전자 ID, 실제 운전자 계정 ID)
- **차량 번호판 (car_plate_number):** `string`, 필수
- **출발지 이름 (departure_location_name):** `string`, 필수 (예: "우리 마을 회관", "마을 입구")
- **출발 시간 (departure_time):** `datetime`, 필수 (ISO 8601 형식)
- **목적지 이름 (destination_location_name):** `string`, 필수 (예: "옆 동네 학교", "시내 버스 터미널")
- **ID (id):** `UUID`, 서버에서 자동 생성

**JSON 데이터 샘플:**

**등록 요청:**

JSON

```
{
  "driver_id": "f0e9d8c7-b6a5-4321-fedc-ba9876543210",
  "car_plate_number": "서울12가1234",
  "departure_location_name": "마을회관",
  "departure_time": "2025-06-01T09:00:00Z",
  "destination_location_name": "시내 학원가"
}
```

**등록 응답/조회:**

JSON

```
{
  "id": "1a2b3c4d-5e6f-7080-90a0-b0c0d0e0f0a0",
  "driver_id": "f0e9d8c7-b6a5-4321-fedc-ba9876543210",
  "car_plate_number": "서울12가1234",
  "departure_location_name": "마을회관",
  "departure_time": "2025-06-01T09:00:00Z",
  "destination_location_name": "시내 학원가"
}
```

#### 5.3. 탑승 정보 (Ride Request)

- **운행경로 정보 (ride_route_id):** `UUID`, 필수 (해당 운행 경로 ID)
- **승객 정보 (passenger_id):** `UUID`, 필수 (탑승을 요청한 승객 ID)
- **탑승 요청 위치 (pickup_request_location_name):** `string`, 필수 (예: "우리 집 앞", "마을 보건소")
- **탑승 시간 (pickup_time):** `datetime`, 필수 (ISO 8601 형식, 운행 경로의 출발 시간보다 늦지 않아야 함)
- **탑승 허용 여부 (is_approved):** `boolean`, 필수 (기본값: `false`, 운전자가 승인하면 `true`)
- **ID (id):** `UUID`, 서버에서 자동 생성

**JSON 데이터 샘플:**

**등록 요청:**

JSON

```
{
  "ride_route_id": "1a2b3c4d-5e6f-7080-90a0-b0c0d0e0f0a0",
  "passenger_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "pickup_request_location_name": "김영희네 집 앞",
  "pickup_time": "2025-06-01T09:05:00Z"
}
```

**등록 응답/조회 (초기 상태):**

JSON

```
{
  "id": "x1y2z3a4-b5c6-d7e8-f9g0-h1i2j3k4l5m6",
  "ride_route_id": "1a2b3c4d-5e6f-7080-90a0-b0c0d0e0f0a0",
  "passenger_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "pickup_request_location_name": "김영희네 집 앞",
  "pickup_time": "2025-06-01T09:05:00Z",
  "is_approved": false
}
```

**승인 후 응답:**

JSON

```
{
  "id": "x1y2z3a4-b5c6-d7e8-f9g0-h1i2j3k4l5m6",
  "ride_route_id": "1a2b3c4d-5e6f-7080-90a0-b0c0d0e0f0a0",
  "passenger_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "pickup_request_location_name": "김영희네 집 앞",
  "pickup_time": "2025-06-01T09:05:00Z",
  "is_approved": true
}
```

### 6. 기능 요구사항

#### 6.1. 승객 관리

- **승객 등록 (POST /passengers)**
    - 새로운 승객 정보를 등록합니다.
    - 요청: 이름, 연락처
    - 응답: 등록된 승객 정보 (ID 포함)

#### 6.2. 운행 경로 관리

- **운행 경로 정보 등록 (POST /ride_routes)**
    - 운전자가 새로운 운행 경로를 등록합니다.
    - 요청: 운전자 ID, 차량 번호판, 출발지 이름, 출발 시간, 목적지 이름
    - 응답: 등록된 운행 경로 정보 (ID 포함)
- **운행 경로 정보 삭제 (DELETE /ride_routes/{route_id})**
    - 특정 운행 경로 정보를 삭제합니다.
    - 요청: 운행 경로 ID (URL 경로 변수)
    - 응답: 성공/실패 메시지 (HTTP 204 No Content 또는 200 OK)
- **운행 경로 정보 수정 (PUT /ride_routes/{route_id})**
    - 특정 운행 경로의 정보를 수정합니다.
    - 요청: 운행 경로 ID (URL 경로 변수), (수정할) 차량 번호판, 출발지 이름, 출발 시간, 목적지 이름
    - 응답: 수정된 운행 경로 정보
- **운행 경로 정보 조회 (GET /ride_routes)**
    - 모든 운행 경로 또는 특정 조건(예: 특정 운전자의 운행 경로, 특정 시간대)에 맞는 운행 경로를 조회합니다.
    - 요청: (선택 사항) `driver_id`, `start_time`, `end_time`, `departure_location_name`, `destination_location_name` (쿼리 파라미터)
    - 응답: 운행 경로 목록

#### 6.3. 탑승 관리

- **탑승 요청 정보 등록 (POST /ride_requests)**
    - 승객이 특정 운행 경로에 대한 탑승을 요청합니다.
    - 요청: 운행 경로 ID, 승객 ID, 탑승 요청 위치, 탑승 시간
    - 응답: 등록된 탑승 요청 정보 (ID 포함, `is_approved`는 `false`)
- **탑승 정보 조회 (GET /ride_requests/{request_id})**
    - 특정 탑승 요청의 상세 정보를 조회합니다.
    - 요청: 탑승 요청 ID (URL 경로 변수)
    - 응답: 탑승 요청 상세 정보
- **탑승 요청정보 조회 (GET /ride_requests)**
    - 모든 탑승 요청 정보 또는 특정 조건(예: 특정 운행 경로의 탑승 요청, 승인 여부)에 맞는 탑승 요청을 조회합니다.
    - 요청: (선택 사항) `ride_route_id`, `passenger_id`, `is_approved` (쿼리 파라미터)
    - 응답: 탑승 요청 목록
- **탑승 승인 (PUT /ride_requests/{request_id}/approve)**
    - 운전자가 특정 탑승 요청을 승인합니다. `is_approved` 필드를 `true`로 변경합니다.
    - 요청: 탑승 요청 ID (URL 경로 변수)
    - 응답: 업데이트된 탑승 요청 정보

### 7. 프로젝트 구조
- HTTP 통신으로 Request/Response를 처리하는 코드는 /controllers/fms_controller.py에 작성한다. 해당 파일안에 이미 코드가 존재할때는 문맥상 가장 적합한 곳을 찾아 수정하고 그렇지 않을때 코드를 추가한다.
- 비즈니스 로직을 담당하는 코드는 /services/fms_service.py에 작성한다. 해당 파일안에 이미 코드가 존재할때는 문맥상 가장 적합한 곳을 찾아 수정하고 그렇지 않을때 코드를 추가한다.
- 데이터 모델을 담당하는 코드는 /domains/passenger.py, /domains/route.py, /domains/trip.py에 작성한다. 해당 파일안에 이미 코드가 존재할때는 문맥상 가장 적합한 곳을 찾아 수정하고 그렇지 않을때 코드를 추가한다.

### 8. 비기능 요구사항

- **성능:**
    - 모든 API는 500ms 이내에 응답해야 합니다.
    - 초기 마을 규모를 고려하여 최소 50명 이상의 동시 접속을 처리할 수 있어야 합니다.
- **확장성:**
    - 향후 마을 수 증가 및 서비스 기능 확장을 고려하여 모듈화된 아키텍처를 지향합니다.
    - API 버전 관리를 통해 서비스 확장에 용이하게 설계합니다.
- **보안:**
    - 모든 통신은 **HTTPS**를 통해 암호화되어야 합니다.
    - 사용자 및 운전자 **인증/인가 메커니즘**을 적용합니다 (예: JWT 토큰).
    - 민감 정보 (연락처, 차량 번호판)는 데이터베이스에 **암호화하여 저장**합니다.
- **안정성:**
    - 서버는 **99.9% 이상의 가용성**을 유지해야 합니다.
    - 오류 발생 시 상세한 **로깅**을 수행하고, 적절한 에러 응답을 반환해야 합니다.
    - 정기적인 **데이터 백업 및 복구** 절차를 수립합니다.
- **유지보수성:**
    - FastAPI의 자동 문서화 기능을 활용하여 **API 명세서**를 제공합니다 (Swagger UI).
    - 일관된 코딩 스타일 및 주석을 사용하여 코드 가독성을 높입니다.
- **LLM 봇 연동:**
    - LLM 봇과의 MCP 통신 규약을 명확히 정의하고, 안정적인 연동을 위한 인터페이스를 제공합니다.


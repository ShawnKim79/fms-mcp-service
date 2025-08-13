# 에이전트 규칙 부록

이 문서는 `.cursor/agent-rules.md`를 보완합니다. 확장 예시, 선택적 세부 지침, 배경 설명을 수집합니다. 기본 동작은 항상 `agent-rules.md`를 따르세요.

## 코드 인용 및 설명 예시
- 인용 형식: `startLine:endLine:filepath`
```
42:58:app/main.py
# ... 일부 코드 생략 ...
app.include_router(api_router, prefix="/api/v1")
# ... 일부 코드 생략 ...
```
- 가독성을 위해 주변 1–2줄만 인용하세요.

## 도구 호출 모범 사례
- 읽기/검색 작업을 병렬로 수행해 대기 시간을 줄이세요.
- 디렉터리 이동 없이 절대 경로를 사용하세요.
- 장시간 실행/백그라운드 프로세스는 실행하지 마세요.

## 코드 에디트 출력 가이드(확장)
- 최소한의 에디트 블록과 1–2문장의 의도 설명을 제공하세요.
- 불필요한 재포맷을 피하고 기존 스타일/들여쓰기를 보존하세요.

## 보안과 비밀 관리 예시
- 비밀번호, 토큰, API 키를 로그/메시지에 노출하지 마세요.
- 샘플 키는 마스킹하거나 더미 값으로 대체하세요.

## 커밋 메시지 확장 규칙
- 권장 접두사: feat, fix, refactor, test, docs, chore, perf, ci
- 본문에서 관련 이슈/PR을 참조할 경우 링크나 번호를 포함하세요.

## 환경 확인 팁
- macOS Homebrew 경로: Apple Silicon은 `/opt/homebrew`, Intel은 `/usr/local`
- Python/uvicorn 버전 불일치 시 `pyproject.toml`과 `requirements.txt`를 확인하세요.

## 테스트/빌드 체크리스트(선택)
- 변경 후 `pytest -q`로 기본 테스트가 통과하는지 확인하세요.
- Dockerfile 변경 시 로컬 빌드/실행으로 검증하세요: `docker build . && docker run ...`
 
## 브랜치 전략
- 기본 브랜치: `main`
- 통합 브랜치(선택): `develop`
- 작업 브랜치: `feature/<id-summary>`, `fix/<id-summary>`, `chore/<summary>`
- 머지 정책: squash merge 권장; 긴 기록은 rebase로 정리

## 커밋 메시지 예시
- feat: 제품 API에 페이지네이션 추가
- fix: 비동기 세션 누수 패치
- chore: 의존성 버전 정리 및 lockfile 갱신
- docs: DB 배포 README 개선

## PR 체크리스트
- [ ] 모든 테스트 통과(`pytest -q`)
- [ ] 린트/포맷 통과
- [ ] 핵심 변경 및 의도(왜)를 설명
- [ ] 리스크/롤백 플랜 기재

## Python 코드 스타일 세부
- 임포트 순서: 표준 라이브러리 → 서드파티 → 로컬, 그룹 간 빈 줄
- 로깅: `logging` 표준 사용; 포맷/레벨은 환경에 맞춰 설정(`utils/logger.py` 참고)
- 예외: 의미 있는 메시지와 도메인 오류를 사용; 포괄적 `except Exception` 지양, 롤백 철저
- 함수 길이: 약 50줄; 복잡해지면 분리
- Pydantic v2 모델 사용, `model_validate`, `ConfigDict(from_attributes=True)` 채택

## FastAPI 관례
- fms_server: `app/controllers/*`의 `APIRouter` 사용, 서비스/도메인 분리
- chatbot: `app/controllers/{slack_controller,mcp_controller}.py` 라우팅, 서비스로 분리
- 스키마: Pydantic 모델 사용, 가능하면 `response_model` 명시
- 미들웨어: 로깅 → CORS → 기타 순서

## DB/ORM 가이드
- 현재 동기 SQLAlchemy 세션 사용(`SessionLocal`); `get_db_session` 의존성으로 주입
- 트랜잭션: 서비스 레이어에서 명시적으로 관리; 예외 시 `rollback()`
- 암호/시크릿: `passlib` 등 해시 적용(예: Passenger.password)
- 인덱스: 조회 패턴 기반 설계; 불필요한 인덱스 제거

## 마이그레이션 정책
- 기본: `db/ddl`에 버전 파일 추가(예: `001_*.sql`), 변경 이력 주석 포함
- 대안: 구조 변경이 잦다면 Alembic 고려

## 테스트 규칙
- fms_server: `tests/` 아래 컨트롤러/서비스 중심 테스트
- 픽스처: DB 세션/시드 데이터 중앙화; 테스트 격리 유지
- 커버리지: 핵심 서비스/컨트롤러 최소 커버리지 확보

## 보안 가이드
- Chatbot은 `.env` 파일로 Slack/MCP 키를 관리, 레포에 시크릿 커밋 금지
- 로그/예외 메시지에 PII/시크릿 노출 금지
- 외부 웹훅/이벤트 엔드포인트는 공개 URL로만 노출(내부 정보 포함 금지)

## 성능/확장성
- DB 풀: `pool_size`, `max_overflow`, `pool_recycle` 튜닝
- 페이지네이션: 기본 상한 설정; 응답 페이로드 최소화
- 배치 처리: 대규모 작업은 청크로 분할해 트랜잭션 압력 완화

## 가시성/로깅
- 레벨: 프로덕션은 INFO, 개발은 DEBUG
- 포맷: 요청–응답 상관 ID 포함; 구조화 로그 선호
- 경고/오류: 알림 대상 정의

## 환경/배포
- Docker: 멀티스테이지 빌드 고려; healthcheck 설정
- 리소스: ulimit/메모리/파일 디스크립터 제한 검토
- 구성: 환경 변수 주입; 불변 이미지를 원칙으로

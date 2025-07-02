import os
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# 데이터베이스 연결 설정
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_USER = os.environ.get("DB_USER", "fms_user")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "fms_password")
DB_NAME = os.environ.get("DB_NAME", "fms")

# 데이터베이스 URL 생성
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 엔진 생성
engine = create_engine(
    url=DATABASE_URL,
    echo=False,  # SQL 쿼리 로깅 비활성화
    pool_pre_ping=True,  # 연결 유효성 검사
    pool_size=5,  # 커넥션 풀 크기
    max_overflow=10  # 최대 추가 연결 수
)

# 세션 팩토리 생성
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=True,
    expire_on_commit=False
)

def get_db_session() -> Session:
    """
    데이터베이스 세션을 생성하고 반환합니다.
    """
    session = SessionLocal()
    try:
        return session
    except Exception as e:
        print(f"Error creating database session: {e}")
        session.close()
        raise

@contextmanager
def get_db_session_context():
    """
    컨텍스트 매니저를 사용하여 데이터베이스 세션을 관리합니다.
    사용 예시:
    with get_db_session_context() as session:
        # 데이터베이스 작업 수행
        session.commit()
    """
    session = SessionLocal()
    try:
        yield session
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()

# def get_db_connection():
#     conn = None
#     try:
#         conn = psycopg2.connect(
#             host=DB_HOST,
#             port=DB_PORT,
#             user=DB_USER,
#             password=DB_PASSWORD,
#             dbname=DB_NAME,
#         )
#         print("Connected to PostgreSQL")
#         return conn
#     except psycopg2.Error as e:
#         print(f"Error connecting to PostgreSQL: {e}")
#         return None

# def close_db_connection(conn):
#     if conn:
#         conn.close()
#         print("Disconnected from PostgreSQL")

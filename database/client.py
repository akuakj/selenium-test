from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from database.config import settings

class DBClient:
    engine: Engine
    db_url: str = settings.database_url_psycopg

    def __init__(self):
        self.engine = create_engine(
            self.db_url,
            echo=False,
            pool_size=5,
            max_overflow=10
        )
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            expire_on_commit=False
        )

    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        session: Session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

client = DBClient()

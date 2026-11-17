import os
import sys
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Cyber123")
DB_NAME = os.getenv("DB_NAME", "blackandwhite_ecosystem")

Base = declarative_base()


def init_engine():
    """Inicializa la conexion a MySQL con creacion automatica de la base de datos."""
    try:
        import pymysql

        conn = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            charset="utf8mb4",
            connect_timeout=2,
        )
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` "
                    f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
                )
            conn.commit()
        finally:
            conn.close()

        encoded_password = quote_plus(DB_PASSWORD)
        mysql_url = f"mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
        eng = create_engine(mysql_url, pool_pre_ping=True, pool_recycle=3600)
        with eng.connect() as test_conn:
            pass
        print(f"[BD] Conectado exitosamente a MySQL ({DB_HOST}:{DB_PORT}/{DB_NAME})")
        return eng
    except Exception as exc:
        print(
            f"[BD] MySQL no disponible en {DB_HOST}:{DB_PORT} ({exc.__class__.__name__}). "
            "Activando base de datos local SQLite para ejecucion inmediata..."
        )
        sqlite_file = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "blackandwhite_ecosystem.db")
        )
        sqlite_url = f"sqlite:///{sqlite_file}"
        eng = create_engine(sqlite_url, connect_args={"check_same_thread": False})
        print(f"[BD] Base de datos local SQLite activa en: {sqlite_file}")
        return eng


engine = init_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

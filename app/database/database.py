from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from sqlalchemy.orm import sessionmaker
from app.database import models
import sys
import io

if sys.version_info[0] == 3 and sys.version_info[1] >= 7:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', write_through=True)
else:
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

def create_database():
    try:
        password = quote_plus("123")

        engine = create_engine(
            f'postgresql+psycopg2://virtual_museum:{password}@localhost/postgres',
            client_encoding='utf8',
            isolation_level="AUTOCOMMIT"
        )

        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 FROM pg_database WHERE datname='cultural_db'"))

            if not result.scalar():
                conn.execute(text("CREATE DATABASE cultural_db WITH ENCODING 'UTF8' TEMPLATE template0"))
                print("База данных cultural_db создана успешно!")
            else:
                print("База данных cultural_db уже существует")

        engine = create_engine(
            f'postgresql+psycopg2://virtual_museum:{password}@localhost/cultural_db',
            client_encoding='utf8',
            pool_pre_ping=True,
            connect_args={
                'connect_timeout': 10,
                'application_name': 'cultural_app'
            }
        )

        return engine

    except Exception as e:
        print(f"Ошибка при создании базы данных: {str(e)}")
        raise

engine = create_database()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    models.Base.metadata.create_all(engine)

    db = SessionLocal()
    try:
        if not db.query(models.Admin).first():
            from app.crud.auth import create_admin
            from app.schemas.auth import AdminCreate
            create_admin(db, AdminCreate(
                login="museum",
                password="thebestadmin",
                role="admin"
            ))
            db.commit()
    finally:
        db.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, text
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from urllib.parse import quote_plus
import sys
import io

Base = declarative_base()

# Настройка кодировки для вывода
if sys.version_info[0] == 3 and sys.version_info[1] >= 7:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', write_through=True)
else:
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

class Exhibit(Base):
    __tablename__ = 'exhibit'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    region = Column(String(100))
    district = Column(String(100))
    place = Column(String(100))
    ethnos = Column(String(100))
    desc = Column(String(1000))
    main_photo = Column(String(255))

    # Связи
    photos = relationship("PhotoExhibit", back_populates="exhibit", cascade="all, delete-orphan")
    linked_exhibits = relationship("OtherExhibit",
                                   foreign_keys="[OtherExhibit.id_exhibit]",
                                   back_populates="exhibit",
                                   cascade="all, delete-orphan")


class PhotoExhibit(Base):
    __tablename__ = 'photos_exhibit'

    id = Column(Integer, primary_key=True)
    photo = Column(String(255), nullable=False)
    id_exhibit = Column(Integer, ForeignKey('exhibit.id', ondelete="CASCADE"))

    exhibit = relationship("Exhibit", back_populates="photos")


class OtherExhibit(Base):
    __tablename__ = 'other_exhibits_exhibit'

    id = Column(Integer, primary_key=True)
    linked_exhibit = Column(Integer, ForeignKey('exhibit.id', ondelete="CASCADE"))
    id_exhibit = Column(Integer, ForeignKey('exhibit.id', ondelete="CASCADE"))

    exhibit = relationship("Exhibit", foreign_keys=[id_exhibit], back_populates="linked_exhibits")
    linked = relationship("Exhibit", foreign_keys=[linked_exhibit])


class Admin(Base):
    __tablename__ = 'admin'

    login = Column(String(50), primary_key=True)
    password_hash = Column(String(255), nullable=False)
    salt = Column(String(100), nullable=False)


class Culture(Base):
    __tablename__ = 'culture'

    id = Column(Integer, primary_key=True)
    type = Column(String(100))
    title = Column(String(255))
    author = Column(String(100))
    model = Column(String(100))
    creation_date = Column(String(50))
    location = Column(String(255))
    desc = Column(String(1000))
    region = Column(String(100))
    district = Column(String(100))
    place = Column(String(100))
    ethnos = Column(String(100))
    main_photo = Column(String(255))

    categories = relationship("CategoryCulture", back_populates="culture", cascade="all, delete-orphan")
    linked_articles = relationship("OtherArticleCulture",
                                   foreign_keys="[OtherArticleCulture.id_culture]",
                                   back_populates="culture",
                                   cascade="all, delete-orphan")


class CategoryCulture(Base):
    __tablename__ = 'categories_culture'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    id_culture = Column(Integer, ForeignKey('culture.id', ondelete="CASCADE"))

    culture = relationship("Culture", back_populates="categories")


class OtherArticleCulture(Base):
    __tablename__ = 'other_articles_culture'

    id = Column(Integer, primary_key=True)
    linked_article = Column(Integer, ForeignKey('culture.id', ondelete="CASCADE"))
    id_culture = Column(Integer, ForeignKey('culture.id', ondelete="CASCADE"))

    culture = relationship("Culture", foreign_keys=[id_culture], back_populates="linked_articles")
    linked = relationship("Culture", foreign_keys=[linked_article])


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


if __name__ == "__main__":
    try:
        engine = create_database()

        Base.metadata.create_all(engine)
        print("Таблицы успешно созданы")

        # Создание тестовых данных
        Session = sessionmaker(bind=engine)
        session = Session()

        admin = Admin(
            login="admin",
            password_hash="hashed_password_here",
            salt="random_salt_here"
        )
        session.add(admin)

        exhibit = Exhibit(
            title="Древняя ваза",
            region="Центральный регион",
            district="Столичный округ",
            place="Археологический музей",
            ethnos="Древние цивилизации",
            desc="Очень древняя ваза с узорами",
            main_photo="vase.jpg"
        )
        session.add(exhibit)

        culture = Culture(
            type="Традиция",
            title="Народный танец",
            author="Народное творчество",
            model="Танцевальная",
            creation_date="XIX век",
            location="Этнографический музей",
            desc="Традиционный народный танец",
            region="Северный регион",
            district="Северный округ",
            place="Деревня Белая",
            ethnos="Северные народы",
            main_photo="dance.jpg"
        )
        session.add(culture)

        session.commit()
        print("Тестовые данные успешно добавлены")

    except Exception as e:
        print(f"Ошибка: {str(e)}")
        if 'session' in locals():
            session.rollback()
    finally:
        if 'session' in locals():
            session.close()
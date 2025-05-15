from enum import Enum as PyEnum
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()

class Exhibit(Base):
    __tablename__ = 'exhibit'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    region = Column(String(100), nullable=True)
    district = Column(String(100), nullable=True)
    place = Column(String(100), nullable=True)
    ethnos = Column(String(100), nullable=True)
    desc = Column(String(1000), nullable=True)
    main_photo = Column(String(255), nullable=True)

    photos = relationship("PhotoExhibit", back_populates="exhibit", cascade="all, delete-orphan")
    linked_exhibits = relationship("OtherExhibit",
                                   foreign_keys="[OtherExhibit.id_exhibit]",
                                   back_populates="exhibit",
                                   cascade="all, delete-orphan")


class PhotoExhibit(Base):
    __tablename__ = 'photos_exhibit'

    id = Column(Integer, primary_key=True)
    photo_path = Column(String(255), nullable=False)  # хранится относительный путь, например uploads/images/name.jpg
    id_exhibit = Column(Integer, ForeignKey('exhibit.id', ondelete="CASCADE"))

    exhibit = relationship("Exhibit", back_populates="photos")


class OtherExhibit(Base):
    __tablename__ = 'other_exhibits_exhibit'

    id = Column(Integer, primary_key=True)
    linked_exhibit_id = Column(Integer, ForeignKey('exhibit.id', ondelete="CASCADE"))
    id_exhibit = Column(Integer, ForeignKey('exhibit.id', ondelete="CASCADE"))

    exhibit = relationship("Exhibit", foreign_keys=[id_exhibit], back_populates="linked_exhibits")
    linked = relationship("Exhibit", foreign_keys=[linked_exhibit_id])


class AdminRole(str, PyEnum):
    ADMIN = "admin"

class Admin(Base):
    __tablename__ = 'admin'

    login = Column(String(50), primary_key=True)
    password_hash = Column(String(255), nullable=False)
    salt = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)


class CultureTypeEnum(str, PyEnum):
    DECORATIVE = "Декоративно-прикладное искусство"
    VERBAL = "Устное народное творчество"
    MUSIC = "Танцевально-музыкальная культура"

class Culture(Base):
    __tablename__ = 'culture'

    id = Column(Integer, primary_key=True, index=True)
    type = Column(SQLEnum(CultureTypeEnum), nullable=False)
    title = Column(String(255), nullable=False)
    author = Column(String(100), nullable=True)
    model = Column(String(100), nullable=True)
    creation_date = Column(String(50), nullable=True)
    location = Column(String(255), nullable=True)
    desc = Column(String(1000), nullable=True)
    region = Column(String(100), nullable=True)
    district = Column(String(100), nullable=True)
    place = Column(String(100), nullable=True)
    ethnos = Column(String(100), nullable=True)
    main_photo = Column(String(255), nullable=True)

    linked_articles = relationship("OtherArticleCulture",
                                   foreign_keys="[OtherArticleCulture.id_culture]",
                                   back_populates="culture",
                                   cascade="all, delete-orphan")


class OtherArticleCulture(Base):
    __tablename__ = 'other_articles_culture'

    id = Column(Integer, primary_key=True)
    linked_article = Column(Integer, ForeignKey('culture.id', ondelete="CASCADE"))
    id_culture = Column(Integer, ForeignKey('culture.id', ondelete="CASCADE"))

    culture = relationship("Culture", foreign_keys=[id_culture], back_populates="linked_articles")
    linked = relationship("Culture", foreign_keys=[linked_article])

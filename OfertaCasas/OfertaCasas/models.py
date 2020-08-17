# https://towardsdatascience.com/a-minimalist-end-to-end-scrapy-tutorial-part-iii-bcd94a2e8bf3
# https://kirankoduru.github.io/python/sqlalchemy-pipeline-scrapy.html
# https://www.accordbox.com/blog/scrapy-tutorial-9-how-use-scrapy-item/
# https://github.com/ryancerf/scrapy-sqlitem
# http://scrapingauthority.com/scrapy-database-pipeline/  (cool)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from scrapy.utils.project import get_project_settings
from sqlalchemy.orm import relationship
from sqlalchemy import (Integer, String, DateTime, Date, Float, Boolean, Text)


Base = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    :return: sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get('CONNECTION_STRING'))

def create_table(engine):
    Base.metadata.create_all(engine)

class HouseAttributes(Base):
    __tablename__ = "house_attributes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column('url', String(999), unique=True)       # URL de la página a la que se extrae información
    location = Column('loc', String(999))               # Nombre la ubicación geografica
    description = Column('description', String(999))    # Descripción ampliada de la vivienda
    bedrooms = Column('bedrooms', String())

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///database/datos.db',
connect_args={'check_same_thread':False})
# recomendable separar BBDD del código creando la carpeta aparte
# todos los ficheros HTML en una carpeta TEMPLATES

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
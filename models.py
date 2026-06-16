from jinja2.nodes import List
import db
from sqlalchemy import Column, Integer, String

# hay q tener en cuenta el CRUD (Create Read Update Delete) para abordar el proyecto
# ==== TABLAS RELACIONALES ====
'''Clase Participante: recoge los datos de los participantes'''
class Participante (db.Base):
    __tablename__ = 'participantes'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    apellidos = Column(String(200), nullable=False)
    edad = Column(Integer, nullable=False)
    nivel_estudios = Column(String(200), nullable=False)
    lengua_materna = Column(String, nullable=False) #integer pq html envía un id numérico
    otras_lenguas = Column(String, nullable=True)

'''Clase Lengua: necesaria para poder mostrar en la pag las lenguas que tenemos
No se crea nada con ella, solo se obtienen los datos de ahí'''
class Lengua (db.Base):
    #creamos una clase Lengua para q entienda q hay una tabla con dicha información
    #de esta tabla, saca 1 unidad de lengua
    __tablename__= 'lenguas'
    id = Column(Integer, primary_key=True) #identificador unico de cada lengua
    nombre = Column(String(200), nullable=False) #contenido, texto max 200 caracteres

def obtener_lenguas():
    #fuera de la clase para q nos devuelva el listado de todas las posibles lenguas
    #no es necesario q este en main.py
    lenguas = db.session.query(Lengua).order_by(Lengua.nombre).all()
    return lenguas

#no es necesario crear clase OtrasLenguas pq también son lenguas pero múltiples
#se guardan en una lista "otras_lenguas" en el html

'''Clase Material: recoge los datos de los materiales'''
class Material (db.Base):
    __tablename__ = 'materiales'
    id = Column(Integer, primary_key=True)
    id_item = Column(String(200), nullable=False)
    audio_material= Column(String(200), nullable=False)
    sign_esp = Column(String, nullable=False)

    opt_a = Column(String, nullable=False)
    sign_a = Column(String, nullable=False)
    opt_b = Column(String, nullable=False)
    sign_b = Column(String, nullable=False)
    opt_c = Column(String, nullable=False)
    sign_c = Column(String, nullable=False)
    opt_d = Column(String, nullable=False)
    sign_d = Column(String, nullable=False)

def obtener_materiales():
    materiales = db.session.query(Material).all()
    return materiales

class Respuestas(db.Base):
    __tablename__ = 'respuestas'
    id = Column(Integer, primary_key=True)
    id_item = Column(String(200), nullable=False)
    id_participante = Column(Integer, nullable=False)
    sign_esp = Column(String(200), nullable=False)
    opt_resp = Column(String, nullable=False)
    sign_resp = Column(String, nullable=False)
    ok = Column(Integer, nullable=False)
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class Localidade(Base):
    __tablename__ = 'Localidade'
    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(10))
    pais = Column(String(255), nullable=False)
    aerodromos = relationship('Aerodromo', back_populates='localidade')
    metars = relationship('Metar', back_populates='localidade')
    previsoes = relationship('Previsao', back_populates='localidade')
    tafs = relationship('Taf', back_populates='localidade')

    def to_dict(self, fields):
        return {field: getattr(self, field) for field in fields if hasattr(self, field)}
    
class Aerodromo(Base):
    __tablename__ = 'Aerodromo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    cidade = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    localidade_id = Column(Integer, ForeignKey('Localidade.id'), nullable=False)
    localidade = relationship('Localidade', back_populates='aerodromos')
    radars = relationship('Radar', back_populates='aerodromo')
    
    def to_dict(self, fields):
        return {field: getattr(self, field) for field in fields if hasattr(self, field)}
    
class Taf(Base):
    __tablename__ = 'Taf'
    id = Column(Integer, primary_key=True, autoincrement=True)
    valida_inicial = Column(DateTime, nullable=False)
    valida_final = Column(DateTime, nullable=False)
    mens = Column(Text)
    recebimento = Column(DateTime, nullable=False)
    localidade_id = Column(Integer, ForeignKey('Localidade.id'), nullable=False)
    localidade = relationship('Localidade', back_populates='tafs')
    
    def to_dict(self, fields):
        return {field: getattr(self, field) for field in fields if hasattr(self, field)}

class Metar(Base):
    __tablename__ = 'Metar'
    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(Text, nullable=False)
    data = Column(DateTime, nullable=False)
    localidade_id = Column(Integer, ForeignKey('Localidade.id'))
    localidade = relationship('Localidade', back_populates='metars')
    
    def to_dict(self, fields):
        return {field: getattr(self, field) for field in fields if hasattr(self, field)}
    
class Previsao(Base):
    __tablename__ = 'Previsao'
    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(DateTime, nullable=False)
    temperatura = Column(Float, nullable=False)
    umidade = Column(Float, nullable=False)
    descricao = Column(Text, nullable=False)
    localidade_id = Column(Integer, ForeignKey('Localidade.id'))
    localidade = relationship('Localidade', back_populates='previsoes')
    
    def to_dict(self, fields):
        return {field: getattr(self, field) for field in fields if hasattr(self, field)}
    
class Radar(Base):
    __tablename__ = 'Radar'
    id = Column(Integer, primary_key=True, autoincrement=True)
    imagem = Column(String(255), nullable=True)
    data = Column(DateTime, nullable=False)
    descricao = Column(Text, nullable=False)
    aerodromo_id = Column(Integer, ForeignKey('Aerodromo.id'))
    aerodromo = relationship('Aerodromo', back_populates='radars')
    
    def to_dict(self, fields):
        return {field: getattr(self, field) for field in fields if hasattr(self, field)}
    
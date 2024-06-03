import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from connection.database_connection import Base, Database
from datetime import datetime, timedelta
from constants.paises import PAISES
import requests

import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")

Base = declarative_base()

class Localidade(Base):
    __tablename__  = 'Localidade'
    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(10))
    pais = Column(String(255), nullable=False)
    aerodromos = relationship('Aerodromo', back_populates='localidade')
    metars = relationship('METAR', back_populates='localidade')
    previsoes = relationship('Previsao', back_populates='localidade')
    tafs = relationship('TAF', back_populates='localidade')
    
    @staticmethod
    def extract():
        all_data = []
        for pais in PAISES:
            url = f"{API_BASE_URL}/aerodromos/?api_key={API_KEY}&pais={pais}"
            response = requests.get(url) 
            if response.status_code == 200:
                data = response.json()
                for item in data["data"]:
                    all_data.append({
                        'cod': item['cod'],
                        'pais': item['pais'],
                    })
        return all_data
    
    @staticmethod   
    def save_data(session):
        localidades_data = Localidade.extract()
        for item in localidades_data:
            localidade = Localidade(
                codigo=item['cod'],
                pais=item['pais']
            )
            session.add(localidade)
        session.commit()

class Aerodromo(Base):
    __tablename__ = 'Aerodromo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    cidade = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    localidade_id = Column(Integer, ForeignKey('localidade.id'))
    localidade = relationship('Localidade', back_populates='aerodromos')
    radars = relationship('Radar', back_populates='aerodromo')
    
    @staticmethod
    def extract():
        all_data = []
        for pais in PAISES:
            url = f"{API_BASE_URL}/aerodromos/?api_key={API_KEY}&pais={pais}"
            response = requests.get(url) 
            if response.status_code == 200:
                data = response.json()
                for item in data["data"]:
                    all_data.append({
                        'id': item['id'],
                        'nome': item['nome'],
                        'cidade': item['cidade'],
                        'lat_dec': item['lat_dec'],
                        'lon_dec': item['lon_dec']
                    })
        return all_data
    
    @staticmethod
    def save_data(session):
        aerodromos_data = Aerodromo.extract()
        for item in aerodromos_data:
            aerodromo = Aerodromo(
                id=item['id'],
                nome=item['nome'],
                codigo=item['cod'],
                pais=item['pais'],
                latitude=float(item['lat_dec']),
                longitude=float(item['lon_dec'])
            )
            session.add(aerodromo)
        session.commit()
    
class Taf(Base):
    # TAF:	id / validade_inicial / validade_final / mens / recebimento
    __tablename__ = 'TAF'
    id = Column(Integer, primary_key=True, autoincrement=True)
    valida_inicial = Column(DateTime, nullable=False)
    valida_final = Column(DateTime, nullable=False)
    mens = Column(Text)
    recebimento = Column(DateTime, nullable=False)
    localidade_id = Column(Integer, ForeignKey('localidade.id'), nullable=False)
    localidade = relationship('Localidade', back_populates='tafs')
    
    @staticmethod
    def extract(localidade_code):
        url = f"{API_BASE_URL}/mensagens/taf/{localidade_code}?api_key={API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data["data"]
        else:
            print(f"Erro ao buscar dados TAF para a localidade {localidade_code} - Status Code: {response.status_code}")
            return []
    
    @staticmethod
    def save_data(session):
        pass #TODO

class Metar(Base):
    __tablename__ = 'METAR'
    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(Text, nullable=False)
    data = Column(DateTime, nullable=False)
    localidade_id = Column(Integer, ForeignKey('localidade.id'))
    localidade = relationship('Localidade', back_populates='metars')
    
    @staticmethod
    def extract(aerodromo_code, start_date, end_date):
        url = f"{API_BASE_URL}/mensagens/metar/{aerodromo_code}?api_key={API_KEY}&data_ini={start_date}&data_fim={end_date}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data["data"]
        else:
            print(f"Erro ao buscar dados METAR para o aeródromo {aerodromo_code} - Status Code: {response.status_code}")
            return []
        
    @staticmethod
    def save_data(session):
        aerodromo_ids = {aerodromo.codigo: aerodromo.id for aerodromo in session.query(Aerodromo).all()}
        start_date = datetime(2021, 1, 1)
        end_date = datetime(2021, 1, 1, 1)
        for aerodromo_code, aerodromo_id in aerodromo_ids.items():
            metar_data = Metar.extract(aerodromo_code, start_date.strftime("%Y%m%d%H"), end_date.strftime("%Y%m%d%H"))
            for item in metar_data["data"]:
                if item != None:
                    metar = Metar(
                        aerodromo_id=aerodromo_id,
                        descricao=item['mens'],
                        data=item['recebimento'],
                    )
                    session.add(metar)
            session.commit()
    
class Previsao(Base):
    __tablename__ = 'Previsao'
    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(DateTime, nullable=False)
    temperatura = Column(Float, nullable=False)
    umidade = Column(Float, nullable=False)
    descricao = Column(Text, nullable=False)
    localidade_id = Column(Integer, ForeignKey('localidade.id'))
    localidade = relationship('Localidade', back_populates='previsoes')
    
    @staticmethod
    def extract():
        url = f"{API_BASE_URL}/mensagem/previsao?api_key={API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
        return data["data"]

class Radar(Base):
    __tablename__ = 'Radar'
    id = Column(Integer, primary_key=True)
    imagem = Column(String(255), nullable=True)
    data = Column(DateTime, nullable=False)
    descricao = Column(Text, nullable=False)
    aerodromo_id = Column(Integer, ForeignKey('aerodromo.id'))
    aerodromo = relationship('Aerodromo', back_populates='radars')
    
    @staticmethod
    def extract():
        all_data = []
        start_date = datetime(2023, 1, 1)
        end_date = datetime.now()
        delta = timedelta(days=1)
        while start_date <= end_date:
            date_str = start_date.strftime("%Y%m%d%H")
            url = f"{API_BASE_URL}/produtos/radar/maxcappi?api_key={API_KEY}&data={date_str}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                for item in data['data']['radar'][0]:
                    descricao = item['nome']
                    if isinstance(descricao, str):
                        descricao = descricao.encode('latin1').decode('utf-8', 'ignore')
                    all_data.append({
                        'id': item['id'], 
                        'imagem': item['path'],
                        'data': item['data'],
                        'descricao':descricao
                    })
            start_date += delta
        return all_data

class Satelite(Base):
    __tablename__ = 'Satelite'
    id = Column(Integer, primary_key=True, autoincrement=True)
    imagem = Column(String(255), nullable=False)
    data = Column(DateTime, nullable=False)
    descricao = Column(Text, nullable=False)
    
    @staticmethod
    def extract():
        all_data = []
        start_date = datetime(2021, 1, 1)
        end_date = datetime.now()
        delta = timedelta(days=1)
        while start_date <= end_date:
            date_str = start_date.strftime("%Y%m%d%H")
            url = f"{API_BASE_URL}/produtos/satelite/visivel?api_key={API_KEY}&data={date_str}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                for item in data:
                    all_data.append({
                        'imagem': item['imagem'],
                        'data': datetime.strptime(item['data'], "%Y-%m-%dT%H:%M:%S"),
                        'descricao': item.get('descricao', '')
                    })
            start_date += delta
        return all_data

db = Database()

if __name__ == "__main__":
    try:
        db.create_tables()
    except Exception as e:
        print(f"Erro ao criar as tabelas: {e}")
    # session = db.get_session()
    # localidade = Localidade.save_data(session=session)
    # session.close()
    
    # aerodromo = Aerodromo.save_data(session=session)
    # session.close()
    
    # session = db.get_session()
    # metars = Metar.save_data(session=session)
    # session.close()
    
    
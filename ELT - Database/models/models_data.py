import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from connection.database_connection import Base, Database
from datetime import datetime, timedelta
from constants.paises import PAISES
from constants.cidades import CIDADES
import requests

import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
logger = logging.getLogger(__name__)

API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")

class Localidade(Base):
    __tablename__ = 'Localidade'
    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(10))
    pais = Column(String(255), nullable=False)
    aerodromos = relationship('Aerodromo', back_populates='localidade')
    metars = relationship('Metar', back_populates='localidade')
    previsoes = relationship('Previsao', back_populates='localidade')
    tafs = relationship('Taf', back_populates='localidade')
    
    @staticmethod
    def extract():
        all_data = []
        for pais in PAISES:
            url = f"{API_BASE_URL}/aerodromos/?api_key={API_KEY}&pais={pais}"
            response = requests.get(url) 
            if response.status_code == 200:
                data = response.json()
                for item in data["data"]:
                    logging.info(f"Extraindo localidade {item['cod']} - {item['pais']}")
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
    localidade_id = Column(Integer, ForeignKey('Localidade.id'), nullable=False)
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
                        'cod' : item['cod'],
                        'cidade': item['cidade'],
                        'lat_dec': item['lat_dec'],
                        'lon_dec': item['lon_dec']
                    })
        return all_data
    
    @staticmethod
    def save_data(session):
        aerodromos_data = Aerodromo.extract()
        for item in aerodromos_data:
            localidade = session.query(Localidade).filter_by(codigo=item['cod']).first()
            aerodromo = Aerodromo(
                id=item['id'],
                nome=item['nome'],
                cidade=item['cidade'],
                latitude=float(item['lat_dec']),
                longitude=float(item['lon_dec']),
                localidade_id=localidade.id
            )
            session.add(aerodromo)
        session.commit()
    
class Taf(Base):
    __tablename__ = 'Taf'
    id = Column(Integer, primary_key=True, autoincrement=True)
    valida_inicial = Column(DateTime, nullable=False)
    valida_final = Column(DateTime, nullable=False)
    mens = Column(Text)
    recebimento = Column(DateTime, nullable=False)
    localidade_id = Column(Integer, ForeignKey('Localidade.id'), nullable=False)
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
        localidades = session.query(Localidade).all()
        # start_date = datetime(2021, 1, 1)
        # end_date = datetime(2021, 1, 1, 1)
        for localidade in localidades:
            taf_data = Taf.extract(localidade.codigo)
            if taf_data:
                for item in taf_data["data"]:
                    taf = Taf(
                        valida_inicial=item['validade_inicial'],
                        valida_final=item['validade_final'],
                        mens=item['mens'],
                        recebimento=item['recebimento'], 
                        localidade_id=localidade.id
                    )
                    session.add(taf)
                session.commit()

class Metar(Base):
    __tablename__ = 'Metar'
    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(Text, nullable=False)
    data = Column(DateTime, nullable=False)
    localidade_id = Column(Integer, ForeignKey('Localidade.id'))
    localidade = relationship('Localidade', back_populates='metars')
    
    @staticmethod
    def extract(localidade_code):
        url = f"{API_BASE_URL}/mensagens/metar/{localidade_code}?api_key={API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data["data"]
        else:
            print(f"Erro ao buscar dados METAR para o aeródromo {localidade_code} - Status Code: {response.status_code}")
            return []
        
    @staticmethod
    def save_data(session):
        localidades = session.query(Localidade).filter(Localidade.id).all()
        # start_date = datetime(2021, 1, 1)
        # end_date = datetime(2021, 1, 1, 1)
        for localidade in localidades:
            metar_data = Metar.extract(localidade.codigo)
            if metar_data["data"]:
                for item in metar_data["data"]:
                    metar = Metar(
                        descricao=item['mens'],
                        data=item['recebimento'],
                        localidade_id=localidade.id
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
    localidade_id = Column(Integer, ForeignKey('Localidade.id'))
    localidade = relationship('Localidade', back_populates='previsoes')
    
    @staticmethod
    def extract(localidade):
        url = f"{API_BASE_URL}/aerodromos/info?api_key={API_KEY}&localidade={localidade}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
        return data["data"]

    @staticmethod
    def save_data(session):
        localidades = session.query(Localidade).filter(Localidade.id > 1677).all()
        for localidade in localidades:
            previsao_data = Previsao.extract(localidade.codigo)
            if previsao_data:
                if 'temperatura' in previsao_data and 'ur' in previsao_data and 'condicoes_tempo' in previsao_data and 'data' in previsao_data:
                    try:
                        temperatura = previsao_data['temperatura'].split('º')[0]
                        umidade = previsao_data['ur'].split('%')[0]
                        previsao = Previsao(
                            data=previsao_data['data'],
                            temperatura=float(temperatura),
                            umidade=float(umidade),
                            descricao=previsao_data['condicoes_tempo'],
                            localidade_id=localidade.id
                        )
                        session.add(previsao)
                        session.commit()
                    except ValueError:
                        pass
class Radar(Base):
    __tablename__ = 'Radar'
    id = Column(Integer, primary_key=True, autoincrement=True)
    imagem = Column(String(255), nullable=True)
    data = Column(DateTime, nullable=False)
    descricao = Column(Text, nullable=False)
    aerodromo_id = Column(Integer, ForeignKey('Aerodromo.id'))
    aerodromo = relationship('Aerodromo', back_populates='radars')
    
    @staticmethod
    def extract():
        all_data = []
        start_date = datetime(2024, 1, 1)
        end_date = datetime.now() - timedelta(days=1)
        current_date = start_date
        
        while current_date <= end_date:
            formatted_date = current_date.strftime('%Y%m%d') + '12'
            url = f"{API_BASE_URL}/produtos/radar/maxcappi?api_key={API_KEY}&data={formatted_date}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json().get("data")
                if data and "radar" in data:
                    for itens in data['radar']:
                        for item in itens:
                            all_data.append({
                                'path': item['path'],
                                'data': item['data'],
                                'nome': item['nome'],
                                'localidade': item['localidade']
                            })
            current_date += timedelta(days=1)
            
        return all_data
            
    
    @staticmethod
    def save_data(session):
        aerodromos = session.query(Aerodromo).all()
        aerodromo_dict = {aerodromo.cidade: aerodromo.id for aerodromo in aerodromos}
        localidade_para_cidade = {v: k for k, v in CIDADES.items()}
        
        radar_data = Radar.extract()
        for item in radar_data:
            cidade = localidade_para_cidade.get(item['localidade'])
            if cidade in aerodromo_dict:
                aerodromo_id = aerodromo_dict[cidade]
                if aerodromo_id:
                    if item['path'] != None and item['data'] != None and item['nome'] != None:
                        radar = Radar(
                            imagem=item['path'],
                            data=item['data'],
                            descricao=item['nome'],
                            aerodromo_id=aerodromo_id
                        )
                        session.add(radar)
                session.commit()
                
db = Database()

if __name__ == "__main__":
    try:
        db.create_tables()
    except Exception as e:
        print(f"Erro ao criar as tabelas: {e}")

    session = db.get_session()
    localidade = Localidade.save_data(session=session)
    session.close()
    
    session = db.get_session()
    aerodromo = Aerodromo.save_data(session=session)
    session.close()
    
    session = db.get_session()
    taf = Taf.save_data(session=session)
    session.close()
    
    session = db.get_session()
    metar = Metar.save_data(session=session)
    session.close()
   
    session = db.get_session()
    radar = Radar.save_data(session=session)
    session.close()
    
    session = db.get_session()
    previsao = Previsao.save_data(session=session)
    session.close()
    
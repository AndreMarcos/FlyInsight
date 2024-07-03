from .base_dao import BaseDAO
from models.models import Localidade, Aerodromo, Metar, Taf, Previsao, Radar
from sqlalchemy.orm import joinedload
# from sqlalchemy import func
import logging

logging.basicConfig(level=logging.DEBUG)

class RelatorioDAO(BaseDAO):
    def get_relatorio(self, localidade, codigo, informacoes, metar_checked, taf_checked, limit, filters):
        logging.debug(f"Parameters - Localidade: {localidade}, Codigo: {codigo}, Informacoes: {informacoes}, METAR: {metar_checked}, TAF: {taf_checked}, Limit: {limit}")
        
        field_to_table = {
            'codigo': Localidade,
            'pais': Localidade,
            'nome': Aerodromo,
            'cidade': Aerodromo,
            'latitude': Aerodromo,
            'longitude': Aerodromo,
            'descricao': Metar,
            'localidade_id': Metar,
            'valida_inicial': Taf,
            'valida_final': Taf,
            'mens': Taf,
            'recebimento': Taf,
            'temperatura': Previsao,
            'umidade': Previsao,
            'imagem': Radar,
            'aerodromo_id': Radar,
        }
        
        query = self.get_session()
        query = query.query(Localidade)
        if localidade:
            query = query.filter(Localidade.pais == localidade).options(
                                                 joinedload(Localidade.aerodromos), 
                                                 joinedload(Localidade.metars), 
                                                 joinedload(Localidade.previsoes), 
                                                 joinedload(Localidade.tafs)
                                                 )
        elif codigo:
            query = query.filter(Localidade.codigo == codigo).options(
                                                 joinedload(Localidade.aerodromos), 
                                                 joinedload(Localidade.metars), 
                                                 joinedload(Localidade.previsoes), 
                                                 joinedload(Localidade.tafs)
                                                )
        if not localidade and not codigo:
            query = query.query(Localidade)
        print(informacoes)
        if any(field in informacoes for field in ['nome', 'cidade', 'latitude', 'longitude']):
            query = query.join(Localidade.aerodromos)
        if metar_checked or any(field in informacoes for field in ['descricao', 'localidade_id']):
            query = query.join(Localidade.metars)
        if taf_checked or any(field in informacoes for field in ['valida_inicial', 'valida_final', 'mens', 'recebimento']):
            query = query.join(Localidade.tafs)
        if any(field in informacoes for field in ['temperatura', 'umidade', 'descricao']):
            query = query.join(Localidade.previsoes)
        if any(field in informacoes for field in ['imagem', 'descricao', 'aerodromo_id']):
            query = query.join(Aerodromo.radars)
        
        localidade_ids = [local.id for local in query.all()]
        logging.debug(f"Localidade IDs: {localidade_ids}")

        for f in filters:
            table = field_to_table[f['field']]
            field = getattr(table, f['field'])
            condition = f['condition']
            value = f['value']
            if condition == "=":
                query = query.filter(field == value)
            elif condition == "!=":
                query = query.filter(field != value)
            elif condition == ">":
                query = query.filter(field > value)
            elif condition == "<":
                query = query.filter(field < value)
            elif condition == ">=":
                query = query.filter(field >= value)
            elif condition == "<=":
                query = query.filter(field <= value)
            elif condition == "LIKE":
                query = query.filter(field.like(f"%{value}%"))
        
        if localidade:
            query = query.filter(Localidade.pais == localidade)
        if codigo:
            query = query.filter(Localidade.codigo == codigo)
            
        results = query.limit(limit).all()
        
        data = []
        for localidade in results:
            local_dict = localidade.to_dict(informacoes)
            if localidade.aerodromos:
                for aerodromo in localidade.aerodromos:
                    local_dict.update(aerodromo.to_dict(informacoes))
                    if aerodromo.radars:
                        for radar in aerodromo.radars:
                            local_dict.update(radar.to_dict(informacoes))
            if localidade.previsoes:
                for previsao in localidade.previsoes:
                    local_dict.update(previsao.to_dict(informacoes))
            if localidade.metars:
                for metar in localidade.metars:
                    local_dict.update(metar.to_dict(informacoes))
            if localidade.tafs:
                for taf in localidade.tafs:
                    local_dict.update(taf.to_dict(informacoes))
            data.append(local_dict)
        logging.debug(f"Result: {data}")
        return data

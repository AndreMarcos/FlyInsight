from .base_dao import BaseDAO
from models.models import Localidade, Aerodromo, Metar, Taf, Previsao, Radar
from sqlalchemy.orm import joinedload
from sqlalchemy import func
import logging

logging.basicConfig(level=logging.DEBUG)

class RelatorioDAO(BaseDAO):
    def get_relatorio(self, localidade, codigo, data_inicio, informacoes, metar_checked, taf_checked, limit):
        logging.debug(f"Parameters - Localidade: {localidade}, Codigo: {codigo}, Data Inicio: {data_inicio}, Informacoes: {informacoes}, METAR: {metar_checked}, TAF: {taf_checked}, Limit: {limit}")

        query = self.get_session()
        query = self.get_session()

        if localidade:
            query = query.query(Localidade).filter(Localidade.pais == localidade).options(
                                                 joinedload(Localidade.aerodromos), 
                                                 joinedload(Localidade.metars), 
                                                 joinedload(Localidade.previsoes), 
                                                 joinedload(Localidade.tafs)
                                                 )
        if codigo:
            query = query.query(Localidade).filter(Localidade.codigo == codigo).options(
                                                 joinedload(Localidade.aerodromos), 
                                                 joinedload(Localidade.metars), 
                                                 joinedload(Localidade.previsoes), 
                                                 joinedload(Localidade.tafs)
                                                )

        # if data_inicio:
        #     data_filter = f"%{data_inicio}%"
        #     if metar_checked:
        #         query = query.join(Metar).filter(func.to_char(Metar.data, 'YYYY-MM-DD').like(data_filter))
        #     if taf_checked:
        #         query = query.join(Taf).filter(func.to_char(Taf.valida_inicial, 'YYYY-MM-DD').like(data_filter))
        #     query = query.join(Previsao).filter(func.to_char(Previsao.data, 'YYYY-MM-DD').like(data_filter))
        #     query = query.join(Aerodromo).join(Radar).filter(func.to_char(Radar.data, 'YYYY-MM-DD').like(data_filter))
        
        localidade_ids = [local.id for local in query.all()]
        logging.debug(f"Localidade IDs: {localidade_ids}")

        result = []
        
        localidades = query.limit(limit).all()
        for localidade in localidades:
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
            result.append(local_dict)
        logging.debug(f"Result: {result}")
        return result

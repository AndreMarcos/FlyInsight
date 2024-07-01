from flask import Flask, request, jsonify
from dao.relatorio_dao import RelatorioDAO
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
db_config = 'postgresql+psycopg2://postgres:820dsVG6HdRXXhUK@198.27.114.55:15432/flyinsight'


@app.route('/relatorio', methods=['GET'])
def get_relatorio():
    localidade = request.args.get('localidade')
    codigo = request.args.get('codigo')
    data_inicio = request.args.get('data_inicio')
    informacoes = request.args.get('informacoes', '').split(',')
    metar_checked = request.args.get('metar') == 'true'
    taf_checked = request.args.get('taf') == 'true'
    limit = request.args.get('limit')

    
    dao = RelatorioDAO(db_config)
    result = dao.get_relatorio(localidade, codigo, data_inicio, informacoes, metar_checked, taf_checked, limit)
    
    return jsonify(result)
    

if __name__ == '__main__':
    app.run(debug=True)
    
    
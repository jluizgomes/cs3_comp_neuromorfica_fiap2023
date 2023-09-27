from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://cs3neuro:cs3neuro2023@localhost/previsao_tempo_amazonia'

db = SQLAlchemy(app)

# Defina o modelo para a tabela do banco de dados
class PrevisaoTempo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Data = db.Column(db.String(255))
    Cidade = db.Column(db.String(255))
    Condicao_do_Tempo_Prevista = db.Column(db.String(255))
    Temperatura_Tendencia = db.Column(db.String(255))
    Temperatura_Minima = db.Column(db.String(255))
    Temperatura_Maxima = db.Column(db.String(255))
    Vento_Velocidade_Minima = db.Column(db.String(255))
    Vento_Velocidade_Maxima = db.Column(db.String(255))
    Vento_Direcao = db.Column(db.String(255))
    Vento_Intensidade = db.Column(db.String(255))

# Rota para configurações (pode ser estendida)
@app.route('/configurations', methods=['POST'])
def create_configuration():
    # Implemente a lógica para configurar a ingestão dinâmica aqui
    # Pode usar um modelo de dados para armazenar as configurações
    return jsonify({"message": "Configuração criada com sucesso"})

# Rota para ler dados do CSV e inserir no banco de dados
@app.route('/read', methods=['POST'])
def read_csv():
    try:
        # Ler o CSV e obter os dados do arquivo especificado
        csv_filename = "data/data_weather.csv"
        df = pd.read_csv(csv_filename)

        # Inserir os dados no banco de dados
        df.to_sql('previsao_tempo', con=db.engine, if_exists='replace', index=False)

        return jsonify({"message": "Dados do CSV lidos e inseridos com sucesso"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=8080)

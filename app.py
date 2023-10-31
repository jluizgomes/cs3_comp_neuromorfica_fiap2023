from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import time
import threading
from functools import lru_cache

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://cs3neuro:cs3neuro2023@localhost/previsao_tempo_amazonia'
db = SQLAlchemy(app)

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

@app.route('/configurations', methods=['POST'])
def create_configuration():
    return jsonify({"message": "Configuração criada com sucesso"})

# Implementando memoization para leitura de CSV
@lru_cache(maxsize=1)
def read_csv_memo(filename):
    return pd.read_csv(filename)

def insert_data_to_db(df):
    df.to_sql('previsao_tempo', con=db.engine, if_exists='replace', index=False)

@app.route('/read', methods=['POST'])
def read_csv():
    start_time = time.time()
    csv_filename = "data/data_weather.csv"

    try:
        # Ler o CSV
        read_start_time = time.time()
        df = read_csv_memo(csv_filename)
        read_end_time = time.time()

        # Usando threading para inserção
        thread = threading.Thread(target=insert_data_to_db, args=(df,))
        insert_start_time = time.time()
        thread.start()
        thread.join()
        insert_end_time = time.time()

        message = {
            "message": "Dados do CSV lidos e inseridos com sucesso",
            "read_time": read_end_time - read_start_time,
            "insert_time": insert_end_time - insert_start_time
        }

        return jsonify(message)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        end_time = time.time()
        print(f"Tempo total de execução: {end_time - start_time} segundos.")

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=8080)
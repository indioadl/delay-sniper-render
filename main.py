import os
import time
import sqlite3
import requests
from flask import Flask, render_template
from threading import Thread

from flask import request as flask_request

app = Flask(__name__)

# Banco de dados SQLite
DB = "logs_delay.db"
def salvar_alerta(esporte, casa, visitante, score, odd):
    try:
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS alertas (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            esporte TEXT,
                            casa TEXT,
                            visitante TEXT,
                            score TEXT,
                            odd REAL,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                        )''')
        cursor.execute("INSERT INTO alertas (esporte, casa, visitante, score, odd) VALUES (?, ?, ?, ?, ?)",
                       (esporte, casa, visitante, score, odd))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[ERRO DB] {e}")

# Página principal (painel)
@app.route('/')
def painel():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT esporte, casa, visitante, score, odd, timestamp FROM alertas ORDER BY id DESC LIMIT 30")
    dados = cursor.fetchall()
    conn.close()
    return render_template("painel.html", alertas=dados)

# Função de delay sniper simulada
def delay_sniper():
    print("BOT DELAY SNIPER INICIADO...")
    while True:
        try:
            esporte = "football"
            casa = "Time A"
            visitante = "Time B"
            score = f"{2}-{1}"
            odd = 2.15

            salvar_alerta(esporte, casa, visitante, score, odd)
            print(f"[ALERTA] {casa} x {visitante} | Odd: {odd}")
            time.sleep(30)
        except Exception as e:
            print(f"[ERRO GERAL] {e}")
            time.sleep(5)

Thread(target=delay_sniper).start()

# Rodar Flask com PORT da Render
port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)
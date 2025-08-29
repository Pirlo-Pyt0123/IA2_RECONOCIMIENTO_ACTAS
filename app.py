from flask import Flask, render_template
import sqlite3
import pandas as pd

app = Flask(__name__)

DB_FILE = "votosN.db"

def obtener_votos():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM resultados", conn)
    conn.close()
    return df

def totales_generales(df):
    """Suma de todos los votos por columna"""
    total = df.sum(numeric_only=True).to_dict()
    return total

@app.route("/")
def index():
    df = obtener_votos()
    votos = df.to_dict(orient="records")  # filas como diccionarios
    totales = totales_generales(df)
    partidos = [c for c in df.columns if c not in ("id","mesa_numero")]
    return render_template("index.html", votos=votos, totales=totales, partidos=partidos)

if __name__ == "__main__":
    app.run(debug=True)

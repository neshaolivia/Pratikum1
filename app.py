import os
import time
import mysql.connector
from flask import Flask

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME", "simpledb"),
        user=os.getenv("DB_USER", "appuser"),
        password=os.getenv("DB_PASSWORD", "apppassword"),
        connection_timeout=5
    )

@app.route('/')
def hello():
    return "Halo dari Flask + Docker + Jenkins!"

@app.route('/db')
def check_database():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        if result and result[0] == 1:
            return "Koneksi MySQL berhasil!"
        return "Koneksi MySQL gagal.", 500

    except mysql.connector.Error as error:
        app.logger.error("MySQL connection failed: %s", error)
        return "Database belum dapat dihubungi.", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

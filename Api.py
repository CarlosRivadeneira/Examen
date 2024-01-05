from flask import Flask, jsonify, request
import pyodbc
import requests

app = Flask(__name__)

server = 'localhost'
database = 'TuBaseDeDatos'
username = 'user'
password = '123'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

@app.route('/api/ciudades2', methods=['GET'])
def get_ciudades2():
    cursor = cnxn.cursor()
    cursor.execute("SELECT nombre, apellido, usuario, ciudad FROM TuTabla")
    rows = cursor.fetchall()

    for row in rows:
        nombre = row[0]
        apellido = row[1]
        usuario = row[2]
        ciudad = row[3]
        response = requests.get(f"https://geocode.xyz/{ciudad}?json=1&auth=247521350360750201282x49376")
        data = response.json()
        if response.status_code == 200:
            cursor.execute("INSERT INTO Ciudades2 (nombre, apellido, usuario, ciudad, longitud, latitud) VALUES (?, ?, ?, ?, ?, ?)",
                           (nombre, apellido, usuario, ciudad, data['longt'], data['latt']))
            cnxn.commit()

    cursor.execute("SELECT nombre, apellido, usuario, ciudad, longitud, latitud FROM Ciudades2")
    rows = cursor.fetchall()

    ciudades = [{"nombre": row[0], "apellido": row[1], "usuario": row[2], "ciudad": row[3], "longitud": row[4], "latitud": row[5]} for row in rows]
    return jsonify(ciudades)

@app.route('/api/catalogo_ciudades', methods=['GET'])
def get_catalogo_ciudades():
    cursor = cnxn.cursor()
    cursor.execute("SELECT DISTINCT ciudad, longitud, latitud FROM Ciudades2")
    rows = cursor.fetchall()

    ciudades = [{"ciudad": row[0], "longitud": row[1], "latitud": row[2]} for row in rows]
    return jsonify(ciudades)

@app.route('/api/ciudades2/apellido/<apellido>', methods=['GET'])
def get_clientes_por_apellido(apellido):
    cursor = cnxn.cursor()
    cursor.execute("SELECT nombre, usuario, ciudad, longitud, latitud FROM Ciudades2 WHERE apellido = ?", (apellido,))
    rows = cursor.fetchall()

    clientes = [{"nombre": row[0], "usuario": row[1], "ciudad": row[2], "longitud": row[3], "latitud": row[4]} for row in rows]
    return jsonify(clientes)

if __name__ == '__main__':
    app.run(port=3000)
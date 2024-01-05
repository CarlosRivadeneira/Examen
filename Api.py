from flask import Flask, jsonify, request
import pyodbc
import requests

app = Flask(__name__)

server = 'localhost'
database = 'TuBaseDeDatos'
username = 'user'
password = '123'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

@app.route('/api/ciudad/<apellido>', methods=['GET'])
def get_ciudad(apellido):
    cursor = cnxn.cursor()
    cursor.execute("SELECT nombre, apellido, usuario, ciudad FROM TuTabla WHERE apellido = ?", apellido)
    row = cursor.fetchone()
    
    if row:
        nombre = row[0]
        apellido = row[1]
        usuario = row[2]
        ciudad = row[3]
        response = requests.get(f"https://geocode.xyz/{ciudad}?json=1&auth=247521350360750201282x49376")
        data = response.json()
        if response.status_code == 200:
            cursor.execute("INSERT INTO Ciudades2 (nombre, apellido, usuario, longitud, latitud) VALUES (?, ?, ?, ?, ?)",
                           (nombre, apellido, usuario, data['longt'], data['latt']))
            cnxn.commit()

        return jsonify(data)
    else:
        return jsonify({"error": "No se encontró la ciudad en la base de datos"})

@app.route('/api/ciudades2', methods=['GET'])
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

if __name__ == '__main__':
    app.run(port=3000)
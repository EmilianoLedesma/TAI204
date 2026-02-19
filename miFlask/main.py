from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)
API_URL = "http://localhost:5000"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    respuesta = requests.get(API_URL + "/v1/usuarios/")
    return jsonify(respuesta.json())

@app.route('/usuarios', methods=['POST'])
def agregar_usuario():
    respuesta = requests.get(API_URL + "/v1/usuarios/")
    usuarios = respuesta.json()['usuarios']

    ultimo_id = 0
    for u in usuarios:
        if u['id'] > ultimo_id:
            ultimo_id = u['id']

    nuevo = request.json
    nuevo['id'] = ultimo_id + 1

    respuesta = requests.post(API_URL + "/v1/usuarios/", json=nuevo)
    return jsonify(respuesta.json())

@app.route('/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    respuesta = requests.delete(API_URL + f"/v1/usuarios/{id}")
    return jsonify(respuesta.json())

if __name__ == '__main__':
    app.run(debug=True, port=5010)

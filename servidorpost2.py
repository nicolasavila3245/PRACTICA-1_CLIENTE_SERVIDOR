from flask import Flask, jsonify, request, render_template
from flask_cors import CORS  # Para permitir peticiones desde el navegador

app = Flask(__name__)
CORS(app)  # Habilita CORS para permitir solicitudes desde el navegador

# Credenciales de autenticación (simuladas)
USUARIO_ADMIN = "admin"
PASSWORD_ADMIN = "admin123"

# Base de datos simulada
base_datos = {
    "usuarios": [
        {"id": 1, "nombre": "jose"},
        {"id": 2, "nombre": "maria"}
    ]
}

# Servir la página HTML
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint de autenticación
@app.route('/login', methods=['POST'])
def login():
    datos = request.json
    if datos.get("usuario") == USUARIO_ADMIN and datos.get("password") == PASSWORD_ADMIN:
        return jsonify({"mensaje": "Autenticación exitosa", "auth": True}), 200
    return jsonify({"error": "Credenciales incorrectas"}), 401

# Obtener lista de usuarios (público)
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    return jsonify(base_datos['usuarios'])

# Agregar un nuevo usuario (requiere autenticación)
@app.route('/usuarios', methods=['POST'])
def agregar_usuario():
    if not verificar_autenticacion():
        return jsonify({"error": "No autorizado"}), 403

    nuevo_usuario = request.json  
    if not nuevo_usuario or 'id' not in nuevo_usuario or 'nombre' not in nuevo_usuario:
        return jsonify({"error": "Datos inválidos"}), 400

    for usuario in base_datos['usuarios']:
        if usuario['id'] == nuevo_usuario['id']:
            return jsonify({"error": "El ID ya existe"}), 400

    base_datos['usuarios'].append(nuevo_usuario)
    return jsonify({"mensaje": "Usuario agregado correctamente"}), 201

# Eliminar un usuario por ID (requiere autenticación)
@app.route('/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    if not verificar_autenticacion():
        return jsonify({"error": "No autorizado"}), 403

    for usuario in base_datos['usuarios']:
        if usuario['id'] == id:
            base_datos['usuarios'].remove(usuario)
            return jsonify({"mensaje": "Usuario eliminado correctamente"}), 200

    return jsonify({"error": "Usuario no encontrado"}), 404

# Función para verificar autenticación
def verificar_autenticacion():
    token = request.headers.get("Authorization")
    return token == "Bearer admin123"

if __name__ == '__main__':
    app.run(port=5000, debug=True)

from flask import Flask, jsonify, request

app = Flask(__name__)

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

# Endpoint de autenticación
@app.route('/login', methods=['POST'])
def login():
    datos = request.json
    if datos.get("usuario") == USUARIO_ADMIN and datos.get("password") == PASSWORD_ADMIN:
        return jsonify({"mensaje": "Autenticación exitosa", "token": "admin_token"}), 200
    return jsonify({"error": "Credenciales incorrectas"}), 401

# Obtener lista de usuarios (acceso público)
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    return jsonify(base_datos['usuarios'])

# Buscar usuario por ID (acceso público)
@app.route('/usuarios/<int:id>', methods=['GET'])
def buscar_usuario(id):
    for usuario in base_datos['usuarios']:
        if usuario['id'] == id:
            return jsonify(usuario)
    
    return jsonify({"error": "Usuario no encontrado"}), 404

# Verificación de autenticación
def verificar_autenticacion():
    token = request.headers.get("Authorization")
    return token == "Bearer admin_token"

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

if __name__ == '__main__':
    app.run(port=5000, debug=True)

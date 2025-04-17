from flask import Flask, jsonify, request

app = Flask(__name__)

usuarios = []  # Lista para almacenar los usuarios

# Ruta GET /info
@app.route("/info", methods=["GET"])
def info():
    return jsonify({
        "funcion": "Gestor de usuarios",  
        "version": "1", 
        "descripcion": "API para gestionar usuarios" 
    })

# Ruta POST /createUser
@app.route("/createUser", methods=["POST"])
def crear_usuario():
    data = request.get_json()
    if "nombre" not in data or "email" not in data:  # Verifica que la info incluya un nombre y un email
        return jsonify({"error": "Se requieren 'nombre' y 'email'."}), 400

    usuario = {
        "id": len(usuarios) + 1,  # Genera un id basado en la cantidad de usuarios en memoria
        "nombre": data["nombre"],
        "email": data["email"],
        "fecha_registro": "2025-04-16T12:00:00Z"  # Fecha de registro fija como ejemplo
    }
    usuarios.append(usuario)
    return jsonify({"mensaje": "El Usuario ha sido creado", "usuario": usuario}), 201

# Ruta GET /usuarios
@app.route("/usuarios", methods=["GET"])
def obtener_usuarios():
    return jsonify({"usuarios": usuarios})  

if __name__ == "__main__":
    app.run(debug=True)

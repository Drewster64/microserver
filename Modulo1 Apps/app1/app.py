from flask import Flask, request

app = Flask(__name__)

# Ruta GET /info
@app.route("/info", methods=["GET"])
def info():
    return {
        "aplicacion": "Proyecto Capstone",
        "version": "1.0",
        "Actividad": "Ejemplo basico de con Flask"
    }

# Ruta POST /mensaje
@app.route("/mensaje", methods=["POST"])
def mensaje():
    data = request.json
    nombre = data.get("nombre", "Usuario")
    return {
        "mensaje": f"Bienvenido '{nombre}'"
    }

if __name__ == "__main__":
    app.run(debug=True)

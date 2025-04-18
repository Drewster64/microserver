from flask import Flask, render_template

app = Flask(__name__)

@app.route('/tareas')
def tareas():
    tareas = [
        "Limpiar muestras",
        "Verificar inventario",
        "Entregar mercancía",
        "Organizar almacén",
        "Recibir mercancía",
        "Enviar mercancía"
    ]
    return render_template('tareas.html', tareas=tareas)

if __name__ == '__main__':
    app.run(debug=True)

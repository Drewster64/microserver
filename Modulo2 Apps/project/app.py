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

@app.route('/empleados')
def empleados():
    empleados_info = [
        {"nombre": "Carlos Pérez", "rol": "Carpintero", "foto": "employee1.jpg"},
        {"nombre": "Ana López", "rol": "Supervisora", "foto": "supervisor.jpg"},
        {"nombre": "Luis Ramírez", "rol": "Carpintero", "foto": "employee2.jpg"},
        {"nombre": "James Díaz", "rol": "Mantenimiento", "foto": "employee3.webp"}
    ]
    return render_template('empleados.html', empleados=empleados_info)

if __name__ == '__main__':
    app.run(debug=True)

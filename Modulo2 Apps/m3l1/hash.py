from flask import Flask, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "clave_secreta"

login_manager = LoginManager(app)
login_manager.login_view = "login"

# Modelo de usuario
class User(UserMixin):
    def __init__(self, id, username, password_hash, role):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.role = role

# Crear hashes de contraseñas
hashed_password_juan = generate_password_hash("secreto")
hashed_password_maria = generate_password_hash("secreto")
hashed_password_link = generate_password_hash("ocarina")
hashed_password_zelda = generate_password_hash("trifuerza")


# Usuarios
users = {
    "juan": User(1, "juan", hashed_password_juan, "admin"),
    "maria": User(2, "maria", hashed_password_maria, "user"),
    "Link": User(3, "Link", hashed_password_link, "user"),
    "Zelda": User(4, "Zelda", hashed_password_zelda, "user")
}

@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if str(user.id) == user_id:
            return user
    return None

# Ruta para login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = users.get(username)
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return f"Bienvenido {current_user.username} con rol {current_user.role}!"
        return "Credenciales incorrectas", 401
    return '''
        <form method="post">
            Usuario: <input type="text" name="username"><br>
            Contraseña: <input type="password" name="password"><br>
            <input type="submit" value="Iniciar sesión">
        </form>
    '''

# Ruta para cerrar sesión
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "Sesión cerrada"

# Ruta protegida
@app.route("/dashboard")
@login_required
def dashboard():
    return f"Hola, {current_user.username}! Bienvenido a tu panel de {current_user.role}."

if __name__ == "__main__":
    app.run(debug=True)

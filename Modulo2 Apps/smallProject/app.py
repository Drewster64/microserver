from flask import Flask, render_template, redirect, url_for, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_principal import Principal, Permission, RoleNeed, Identity, AnonymousIdentity, identity_loaded, identity_changed

app = Flask(__name__)
app.config["SECRET_KEY"] = "mi_clave_secreta"

# Inicializar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Inicializar Flask-Principal
principals = Principal(app)

# Base de datos simulada de usuarios
usuarios = {
    "emafranco@tbtmr.com": {"password": "admin123", "rol": "admin"},
    "Drewvalentin@tbtmr.com": {"password": "tester123", "rol": "tester"},
    "benmartinez@tbtmr.com": {"password": "employee123", "rol": "employee"},
    "joselopez@tbtmr.com": {"password": "user123", "rol": "user"}
}

# Permisos por rol
admin_permission = Permission(RoleNeed("admin"))
tester_permission = Permission(RoleNeed("tester"))
employee_permission = Permission(RoleNeed("employee"))
user_permission = Permission(RoleNeed("user"))

# Permiso combinado para developer
developer_permission = Permission(RoleNeed("admin"), RoleNeed("tester"), RoleNeed("employee"))

# Formulario de Login
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

# Clase User para Flask-Login
class User(UserMixin):
    def __init__(self, id):
        self.id = id

    @staticmethod
    def get(user_id):
        return User(user_id)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Cargar identidad y asignar roles
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    identity.user = current_user
    if current_user.is_authenticated:
        user_id = current_user.get_id()
        rol = usuarios[user_id]["rol"]
        identity.provides.add(RoleNeed(rol))

# Ruta de login
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if username in usuarios:
            user_data = usuarios[username]
            if user_data["password"] == password:
                user = User(username)
                login_user(user)
                identity_changed.send(app, identity=Identity(user.id))

                rol = user_data["rol"]
                if rol in ["admin", "tester", "employee"]:
                    return redirect(url_for("developer"))
                elif rol == "user":
                    return redirect(url_for("user_page"))
            else:
                flash(f"Contraseña incorrecta para {user_data['rol']}", "danger")
        else:
            flash("Usuario no encontrado", "danger")

    return render_template("index.html.jinja2", form=form)

# Ruta de logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    identity_changed.send(app, identity=AnonymousIdentity())
    return redirect(url_for("login"))

# Página principal
@app.route("/home")
@login_required
def home():
    return render_template("home.html", message=current_user.id)

# Página protegida para admin/tester/employee
@app.route("/developer")
@login_required
@developer_permission.require(http_exception=403)
def developer():
    return render_template("developer.html", usuario=current_user.id)

# Página exclusiva para user
@app.route("/user_page")
@login_required
@user_permission.require(http_exception=403)
def user_page():
    return render_template("user.html", usuario=current_user.id)

# Página de error 403
@app.errorhandler(403)
def access_denied(e):
    return render_template("403.html"), 403

# Ejecutar la app
if __name__ == "__main__":
    app.run(debug=True)

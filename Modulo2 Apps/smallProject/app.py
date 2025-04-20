from flask import Flask, render_template, redirect, url_for, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config["SECRET_KEY"] = "mi_clave_secreta"

login_manager = LoginManager()
login_manager.init_app(app)

# Simula la funcionalidad de una base de datos de usuarios
usuarios = {
    "emafranco@tbtmr.com": {"password": "admin123", "rol": "admin"},
    "Drewvalentin@tbtmr.com": {"password": "tester123", "rol": "tester"},
    "benmartinez@tbtmr.com": {"password": "employee123", "rol": "employee"},
    "joselopez@tbtmr.com": {"password": "user123", "rol": "user"}
}

# Definimos el formulario de login
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

# Definir los usuarios
class User(UserMixin):
    def __init__(self, id):
        self.id = id

    @staticmethod
    def get(user_id):
        return User(user_id)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

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



# Ruta de home.html
@app.route("/home")
@login_required
def home():
    return render_template("home.html", message=current_user.id)

# Ruta para logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/developer")
@login_required
def developer():
    return render_template("developer.html", usuario=current_user.id)

@app.route("/user_page")
@login_required
def user_page():
    return render_template("user.html", usuario=current_user.id)


if __name__ == "__main__":
    app.run(debug=True)

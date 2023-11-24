from flask import Flask ,Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user
from . import login_manager
from .models import User
from .forms import LoginForm
from . import db_manager as db
from .forms import  CreateUserForm, LoginForm
from werkzeug.security import check_password_hash, generate_password_hash
from .helper_role import notify_identity_changed
from .helper_mail import MailManager
from datetime import datetime
import secrets

# Blueprint
auth_bp = Blueprint(
    "auth_bp", __name__, template_folder="templates", static_folder="static"
)

@auth_bp.route('/profile', methods=["GET"])
@login_required
def profile():
    return render_template('users/profile.html')

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # Si ja està autenticat, sortim d'aquí
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.item_list"))

    form = LoginForm()
    if form.validate_on_submit(): # si s'ha enviat el formulari via POST i és correcte
        name = form.name.data
        plain_text_password = form.password.data

        user = load_user(name)

        if user and check_password_hash(user.password, plain_text_password):
            # aquí és crea la cookie
            login_user(user)
            notify_identity_changed()
            return redirect(url_for("main_bp.init"))

        # si arriba aquí, és que no s'ha autenticat correctament
        return redirect(url_for("auth_bp.login"))
    
    return render_template('users/login.html', form = form)

@login_manager.user_loader
def load_user(name):
    if name is not None:
        # select amb 1 resultat o cap
        user_or_none = db.session.query(User).filter(User.name == name).one_or_none()
        return user_or_none
    return None

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("auth_bp.login"))

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth_bp.login"))

@auth_bp.route('/verify/<name>/<email_token>', methods=["GET"])
def verify(name, email_token):
    verify = User.query.get_or_404(email_token)
    if verify:
        user = User.query.get_or_404(name)
        user.verify = 'True'
        user.updated = datetime.utcnow()
        db.session.commit()
        return redirect(url_for("auth_bp.login", message = "Email verificado con éxito"))


@auth_bp.route('/register', methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.item_list"))
    form = CreateUserForm()
    new_user = User()
    
    if request.method == 'GET':
        
        return render_template('users/register.html', form = form)
    elif request.method == 'POST' and form.validate_on_submit() :
        if form.password.data == form.passConfirmation.data:
            form.populate_obj(new_user)
            token = secrets.token_urlsafe(20)
            new_user.email_token = token
            new_user.verified = 'false'
            new_user.password= generate_password_hash(new_user.password)
            db.session.add(new_user)
            db.session.commit()
            msg = f"""

            Accede a esta página para verificar el mail: http://127.0.0.1:5000/verify/{new_user.name}/{token}
"""
            MailManager.send_contact_msg(msg, new_user.name, new_user.email)
            return render_template('users/login.html', message = "Se te ha enviado un correo de verificación.")
        else:
          return render_template('users/register.html', form = form)  
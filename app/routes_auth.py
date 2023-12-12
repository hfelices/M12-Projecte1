from flask import Flask ,Blueprint, render_template, flash, redirect, url_for, request ,current_app
from flask_login import current_user, login_user, login_required, logout_user
from . import login_manager , mail_manager as mail
from .models import User
from .forms import LoginForm
from . import db_manager as db , logger
from .forms import  CreateUserForm, LoginForm, ResendForm ,ProfileForm
from werkzeug.security import check_password_hash, generate_password_hash
from .helper_role import notify_identity_changed
from datetime import datetime
import secrets

# Blueprint
auth_bp = Blueprint(
    "auth_bp", __name__, template_folder="templates", static_folder="static"
)

@auth_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = ProfileForm(obj=current_user)

    if form.validate_on_submit():
        current_user.name = form.name.data

        if current_user.email != form.email.data:
            current_user.email = form.email.data
            current_user.verified = 'false'
            token = secrets.token_urlsafe(20)
            current_user.email_token = token
            msg = f"""

            Accede a esta página para verificar el mail: http://127.0.0.1:5000/verify/{current_user.name}/{token}
"""         
            mail.send_contact_msg(msg, current_user.name, form.email.data)

        if form.password.data:
            hashed_password = generate_password_hash(form.password.data)
            current_user.password = hashed_password

        db.session.commit()
        logout_user()
        return redirect(url_for('auth_bp.profile'))

    return render_template('/users/profile.html', form=form)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # Si ja està autenticat, sortim d'aquí
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.item_list"))

    form = LoginForm()
    if form.validate_on_submit(): #si s'ha enviat el formulari via POST i és correcte
        name = form.name.data
        plain_text_password = form.password.data
        logger.debug(f"Usuari {name} intenta autenticar-se")

        user = load_user(name)
        

        if user and check_password_hash(user.password, plain_text_password) and user.verified == 'true':
            # aquí és crea la cookie
            login_user(user)
            notify_identity_changed()
            logger.info(f"Usuari {name} s'ha autenticat correctament")
            return redirect(url_for("main_bp.init"))
        if user:    
            if user.verified != 'true' :
                message = "Debe verificar el correo"
            elif not check_password_hash(user.password, plain_text_password):
                logger.warning(f"Usuari {name} no s'ha autenticat correctament")
                message = "Nombre de usuario o contraseña incorrectos"
            # si arriba aquí, és que no s'ha autenticat correctament
            return render_template("users/login.html", form = form, message = message)
        
    return render_template('users/login.html', form = form , )

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
            mail.send_contact_msg(msg, new_user.name, new_user.email)
            form = LoginForm()
            return render_template('users/login.html', message = "Se te ha enviado un correo de verificación.", form = form )
            return render_template('users/register.html', form = form)  
        
@auth_bp.route('/verify/<name>/<token>', methods=["GET"])
def verify(name, token):
    form = LoginForm()
    verify = db.session.query(User).filter(User.email_token == token).one_or_none()
    if verify:
        user = db.session.query(User).filter(User.name == name).one_or_none()
        user.verified = 'true'
        user.updated = datetime.utcnow()
        db.session.commit()
        return render_template("users/login.html", message = "Email verificado con éxito" ,form = form)
    else:
        return render_template("users/login.html", message = "Error al verificar" , form = form)

















@auth_bp.route('/resend', methods=["GET","POST"])
def resend():
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.item_list"))

    form = ResendForm()
    if request.method == 'GET':
        return render_template('users/resend.html' , form = form )
    elif request.method == 'POST'and form.validate_on_submit() :
        email = form.email.data
        user =  User.query.filter_by(email = email).first()
        
        print(f"\033[93m{user.name}\033[0m")
        if check_password_hash(user.password, form.password.data):
            print(f"\033[93m entra \033[0m")
            token = secrets.token_urlsafe(20)
            user.email_token = token
            user.verified = 'false'
            db.session.commit()
            msg = f"""

            Accede a esta página para verificar el mail: http://127.0.0.1:5000/verify/{user.name}/{token}
"""         
            mail.send_contact_msg(msg, user.name, user.email)
    
            flash('Correo de verificación enviado', 'success')
            return redirect(url_for("auth_bp.login"))
        else:
            flash('Correo o contraseña incorrectos', 'success')
            return redirect(url_for("auth_bp.resend"))
        

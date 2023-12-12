from flask import Flask ,Blueprint, render_template, flash, redirect, url_for, request ,current_app
from flask_login import current_user, login_user, login_required, logout_user
from . import login_manager
from .models import User
from .forms import LoginForm
from . import db_manager as db
from sqlalchemyseed import load_entities_from_json
from sqlalchemyseed import Seeder
from .forms import  CreateUserForm, LoginForm, BanForm,UnBanForm
from werkzeug.security import check_password_hash, generate_password_hash
from os import path
import csv
from io import TextIOWrapper
from . import db_manager as db
from .models import Product, Category, User, Ban
from .helper_role import requireAdminRole, requireModeratePermission

basedir = path.abspath(path.dirname(__file__))


# Blueprint
admin_bp = Blueprint(
    "admin_bp", __name__, template_folder="templates", static_folder="static"
)

@admin_bp.route('/admin/products/<product_id>/ban', methods=['POST'])
@login_required
@requireModeratePermission.require(http_exception=403)
def ban(product_id):
    form = BanForm()
    if form.validate_on_submit():
        product = db.session.query(Product).filter(Product.id == product_id).one_or_none()
        if product:
            ban = Ban()
            form.populate_obj(ban)
            
            db.session.add(ban)
            db.session.commit()
            
            return redirect(url_for('main_bp.init'))
        return redirect(url_for('main_bp.init'))
    return redirect(url_for('main_bp.init'))

@admin_bp.route('/admin/products/<product_id>/unban', methods=['POST'])
@login_required
@requireModeratePermission.require(http_exception=403)
def unban(product_id):
    form = UnBanForm()
    if request.method == "POST" and form.validate_on_submit():
        product = Ban.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for('main_bp.init'))
    return redirect(url_for('main_bp.init'))

@admin_bp.route('/admin')
@login_required
@requireModeratePermission.require(http_exception=403)
def admin_index():
    user = current_user.role
    return render_template('admin/index.html', role = user)

@admin_bp.route('/admin/users')
@login_required
@requireAdminRole.require(http_exception=403)
def admin_users():
    users = db.session.query(User).all()
    return render_template('admin/users_list.html', users=users)

# Upload CSV
@admin_bp.route('/admin/tools', methods=["GET","POST"])
@login_required
@requireAdminRole.require(http_exception=403)
def admin():
    if request.method == 'POST':
        table = request.form['table']
        if(table == 'users'):
            csv_file = request.files['file']
            csv_file = TextIOWrapper(csv_file, encoding='utf-8')
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                newUser = User(id=row[0], name=row[1], email=row[2],password=generate_password_hash(row[3]))
                db.session.add(newUser)
                db.session.commit()
        elif(table == 'products'):
            csv_file = request.files['file']
            csv_file = TextIOWrapper(csv_file, encoding='utf-8')
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                newProduct = Product(id=row[0], title=row[1],description=row[2],photo=row[3],price=row[4],category_id=row[5],seller_id=row[1])
                db.session.add(newProduct)
                db.session.commit()
        elif(table == 'categories'):
            csv_file = request.files['file']
            csv_file = TextIOWrapper(csv_file, encoding='utf-8')
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                newCategory = Category(id=row[0], name=row[1],slug=row[2])
                db.session.add(newCategory)
                db.session.commit()
        elif(table== 'hash'):
            users = User.query.all()
            for user in users:
                user.password = generate_password_hash("user.password")
            db.session.commit()
        elif(table== 'categories_seed'):
            
            # load entities
            entities = load_entities_from_json(f"{basedir}'/categories.json'")
            # Initializing Seeder
            seeder = Seeder(db.session)
            # Seeding
            seeder.seed(entities)
            # Committing
            db.session.commit()  
        return redirect(url_for('admin_bp.admin'))
    return render_template('admin/admin_tools.html')
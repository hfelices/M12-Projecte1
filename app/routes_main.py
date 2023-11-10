from flask import Flask ,Blueprint, render_template, flash, redirect, url_for, request
import os
import csv
from io import TextIOWrapper
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
from . import db_manager as db
from .models import Product, Category, User
from .forms import ProductForm, DeleteProductForm
from .config import Config
from flask_login import LoginManager, current_user, login_required
from werkzeug.security import generate_password_hash


ALLOWED_EXTENSIONS = Config.ALLOWED_EXTENSIONS
UPLOAD_FOLDER = Config.UPLOAD_FOLDER
# Comando para iniciar la app flask
# flask --app .\index.py run



# Blueprint
main_bp = Blueprint(
    "main_bp", __name__, template_folder="templates", static_folder="static"
)
# Login manager
login_manager = LoginManager()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main_bp.route("/")
def init():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.item_list'))
    else:
        return redirect(url_for("auth_bp.login"))
    

# Llistar productes
@main_bp.route('/products', methods=["GET"])
@login_required
def item_list():
    deleteForm = DeleteProductForm()
    if request.method == 'GET':
        items = Product.query.all()
        return render_template('products/list.html', items=items, deleteForm=deleteForm)

# Crear nou producte
@main_bp.route('/products/create', methods=["GET", "POST"])
@login_required
def create_item():
    categories = Category.query.all()
    form = ProductForm()
    form.category_id.choices=[(categoria.id, categoria.name) for categoria in categories]
    if form.validate_on_submit(): # si s'ha fet submit al formulari
        # he de crear un nou item
        
        # dades del formulari a l'objecte item
        new_product = Product()
        form.populate_obj(new_product)
        # insert!
        

        file = form.photo.data
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            new_product.photo = filename
            file.save(os.path.join(UPLOAD_FOLDER, filename))

        db.session.add(new_product)
        db.session.commit()
        
        return redirect(url_for('main_bp.item_list'))
    else: 
        return render_template('products/create-update-product.html', form = form)

# Editar productes
@main_bp.route('/products/update/<int:id>', methods=["GET", "POST"])
@login_required
def update_item(id):
    categories = Category.query.all()
    product = Product.query.get_or_404(id)
    form = ProductForm(obj = product)
    form.category_id.choices=[(categoria.id, categoria.name) for categoria in categories]
        
    if request.method == 'GET' :
        categories = Category.query.all()
        
        return render_template('products/create-update-product.html', categories=categories, product=product, form = form)
    elif request.method == 'POST' and form.validate_on_submit():
        # he de crear un nou item
        
        # dades del formulari a l'objecte item
        new_product = Product.query.get_or_404(id)
        form.populate_obj(new_product)
        # insert!
        
        file = form.photo.data
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            new_product.photo = filename
            file.save(os.path.join(UPLOAD_FOLDER, filename))
        
        new_product.updated = datetime.utcnow()

        db.session.commit()

    return redirect(url_for('main_bp.item_list'))

# Eliminar productes
@main_bp.route("/products/delete/<int:id>", methods=["POST"])
@login_required
def delete_item(id):
    product = Product.query.get_or_404(id)
    form = DeleteProductForm(obj = product)
    
    if request.method == "POST" and form.validate_on_submit():
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for("main_bp.item_list"))

    return render_template("/products/list.html")
        
# Detall de producte
@main_bp.route('/products/<int:id>', methods=["GET"])
@login_required
def show_item(id):
    deleteForm = DeleteProductForm()
    if request.method == 'GET':
        item = Product.query.get(id)
        return render_template('products/details.html', item=item , deleteForm=deleteForm)
    


# Upload CSV
@main_bp.route('/admin', methods=["GET","POST"])
# @login_required
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
        elif(request.form['table']== 'hash'):
            users = User.query.all()
            for user in users:
                user.password = generate_password_hash("user.password")
            db.session.commit()
        return redirect(url_for('main_bp.admin'))
    return render_template('admin/admin.html')



    

    

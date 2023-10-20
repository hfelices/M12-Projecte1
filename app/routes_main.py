from flask import Flask ,Blueprint, render_template, flash, redirect, url_for, request
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
from . import db_manager as db
from .models import Product, Category, User
# Comando para iniciar la app flask
# flask --app .\index.py run

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'app/static/uploads'


# Blueprint
main_bp = Blueprint(
    "main_bp", __name__, template_folder="templates", static_folder="static"
)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main_bp.route("/")
def hello_world():
    return redirect(url_for('main_bp.item_list'))

# Llistar productes
@main_bp.route('/products', methods=["GET"])
def item_list():
    if request.method == 'GET':
        items = Product.query.all()
        return render_template('products/list.html', items=items)

# Crear nou producte
@main_bp.route('/products/create', methods=["GET", "POST"])
def create_item():
    if request.method == 'GET':
        categories = Category.query.all()
        return render_template('products/create-update-product.html', categories=categories)
    elif request.method == 'POST':
        form_data = request.form
        file = request.files.get("foto")
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            photo = filename
        else:
            photo = None  

        new_product = Product(
            title=form_data["nombre"],
            description=form_data["descripcion"],
            photo=photo,
            price=form_data["precio"],
            category_id=form_data["categoria"],
            seller_id='1',  
            created=datetime.utcnow(),
            updated=datetime.utcnow()
        )

        db.session.add(new_product)
        db.session.commit()

    return redirect(url_for('main_bp.item_list'))


# Editar productes
@main_bp.route('/products/update/<int:id>', methods=["GET", "POST"])
def update_item(id):
    if request.method == 'GET':
        categories = Category.query.all()
        product = Product.query.get_or_404(id)
        return render_template('products/create-update-product.html', categories=categories, product=product)
    elif request.method == 'POST':
        form_data = request.form
        file = request.files.get("foto")
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            photo = filename
        else:
            photo = form_data["photo"]

        product = Product.query.get_or_404(id)
        product.title = form_data["nombre"]
        product.description = form_data["descripcion"]
        product.photo = photo
        product.price = form_data["precio"]
        product.category_id = form_data["categoria"]
        product.updated = datetime.utcnow()

        db.session.commit()

    return redirect(url_for('main_bp.item_list'))

# Eliminar productes
@main_bp.route("/products/delete/<int:id>", methods=["POST"])
def delete_item(id):
    product = Product.query.get_or_404(id)

    if request.method == "POST":
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for("main_bp.item_list"))

    return render_template("/products/list.html")

# Detall de producte
@main_bp.route('/products/<int:id>', methods=["GET"])
def show_item(id):
    if request.method == 'GET':
        item = Product.query.get(id)
        return render_template('products/details.html', item=item)
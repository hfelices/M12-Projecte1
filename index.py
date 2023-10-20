from flask import Flask , render_template, flash, redirect, url_for, request
import sqlite3
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename

# Comando para iniciar la app flask
# flask --app .\index.py run

app = Flask(__name__)

DATABASE = 'database.db'
UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def now(): return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + basedir + "/" + DATABASE
app.config["SQLALCHEMY_ECHO"] = True

basedir = os.path.abspath(os.path.dirname(__file__)) 


db = SQLAlchemy()
db.init_app(app)

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    photo = db.Column(db.Text)
    price = db.Column(db.DECIMAL(10, 2), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created = db.Column(db.DATETIME, default=now(), nullable=False)
    updated = db.Column(db.DATETIME, default=now(), onupdate=now(), nullable=False)

    category = db.relationship('Category', backref='products')
    seller = db.relationship('User', backref='products')

class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    slug = db.Column(db.Text, unique=True, nullable=False)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    created = db.Column(db.DATETIME, default=now(), nullable=False)
    updated = db.Column(db.DATETIME, default=now(), onupdate=now(), nullable=False)

    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def hello_world():
    return redirect(url_for('item_list'))

# Llistar productes
@app.route('/products', methods=["GET"])
def item_list():
    if request.method == 'GET':
        items = Product.query.all()
        return render_template('products/list.html', items=items)

# Crear nou producte
@app.route('/products/create', methods=["GET", "POST"])
def create_item():
    if request.method == 'GET':
        categories = Category.query.all()
        return render_template('products/create-update-product.html', categories=categories)
    elif request.method == 'POST':
        form_data = request.form
        file = request.files.get("foto")
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            photo = filename
        else:
            photo = None  # Otra opción podría ser usar la foto por defecto o lanzar un error

        new_product = Product(
            title=form_data["nombre"],
            description=form_data["descripcion"],
            photo=photo,
            price=form_data["precio"],
            category_id=form_data["categoria"],
            seller_id='1',  # Aquí deberías establecer el ID del vendedor adecuado
            created=datetime.utcnow(),
            updated=datetime.utcnow()
        )

        db.session.add(new_product)
        db.session.commit()

    return redirect(url_for('item_list'))


# Editar productes
@app.route('/products/update/<int:id>', methods=["GET", "POST"])
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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
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

    return redirect(url_for('item_list'))

# Eliminar productes
@app.route("/products/delete/<int:id>", methods=["POST"])
def delete_item(id):
    product = Product.query.get_or_404(id)

    if request.method == "POST":
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for("item_list"))

    return render_template("/products/list.html")

# Detall de producte
@app.route('/products/<int:id>', methods=["GET"])
def show_item(id):
    if request.method == 'GET':
        item = Product.query.get(id)
        return render_template('products/details.html', item=item)
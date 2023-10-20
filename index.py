from flask import Flask , render_template, flash, redirect, url_for, request
import sqlite3
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename


app = Flask(__name__)

DATABASE = 'database.db'
UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def now(): return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__)) 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + basedir + "/" + DATABASE

app.config["SQLALCHEMY_ECHO"] = True

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




# Comando para iniciar la app flask
# flask --app .\index.py run

@app.route("/")
def hello_world():
    return redirect(url_for('item_list'))



def get_db_connection():

    con = sqlite3.connect(DATABASE)
    # https://docs.python.org/3/library/sqlite3.html#how-to-create-and-use-row-factories
    con.row_factory = sqlite3.Row
    return con

def get_table(table):
    with get_db_connection() as con:
            res = con.execute(f"SELECT * from {table}")
            items = res.fetchall()
            return items

def get_item(id):
    with get_db_connection() as con:
            res = con.execute(f"SELECT * FROM products WHERE id={id}")
            item = res.fetchone()
            return item           

@app.route('/products', methods=["GET","POST"])
def item_list():
    if request.method == 'GET':
        items = get_table('products')
        return render_template('products/list.html', items = items)
    elif request.method == 'POST':
        print('POST')


@app.route('/products/create', methods=["GET","POST"])
def create_item():
    if request.method == 'GET':
        items = get_table('categories')
        return render_template('products/create-update-product.html', categories = items)
    elif request.method == 'POST':
        d = request.form
        file = request.files["foto"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
        with get_db_connection() as con:
            cursor = con.cursor()
            sentencia_sql = '''
    INSERT INTO products (title, description,photo,price,category_id,seller_id,created,updated)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
'''
            dades=(d["nombre"], d["descripcion"], file.filename, d["precio"], d["categoria"], '1', now(),now())
            cursor.execute(sentencia_sql,dades)
            con.commit()
            

    return redirect(url_for('item_list'))



@app.route('/products/update/<int:id>', methods=["GET","POST"])
def update_item(id):
    if request.method == 'GET':
        items = get_table('categories')
        with get_db_connection() as con:    
            res = con.execute(f"SELECT * from  products where id =?",(id,))
            product =  res.fetchone()
            app.logger.info(product)
        return render_template('products/create-update-product.html', categories = items, product = product)
    elif request.method == 'POST':
        d = request.form
        if request.files["foto"]:
            file = request.files["foto"]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                photo = file.filename
        else:
                photo = request.form["photo"]
        with get_db_connection() as con:
            cursor = con.cursor()
            sentencia_sql = f'''
        UPDATE products
        SET title = ?, description = ?, photo = ?, price = ?, category_id = ?,
            seller_id = ?, updated = ?
        WHERE id = {id}
    '''
            dades = (d["nombre"], d["descripcion"], photo, d["precio"], d["categoria"], '1', now())
            cursor.execute(sentencia_sql,dades)
            con.commit()
            

    return redirect(url_for('item_list'))


@app.route("/products/delete/<int:id>", methods=["GET", "POST"])
def delete_item(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    product = cursor.execute("SELECT * FROM products WHERE id = ?", (id,)).fetchone()

    if product is None:
        return "Producto no encontrado", 404

    if request.method == "POST":
        cursor.execute("DELETE FROM products WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return redirect(url_for("item_list"))

    conn.close()
    return render_template("/products/list.html")


@app.route('/products/<int:id>', methods=["GET"])
def show_item(id):
    if request.method == 'GET':
        item = get_item(id)
        return render_template('products/details.html', item = item)
    
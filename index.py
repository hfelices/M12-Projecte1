from flask import Flask , render_template, redirect, url_for
import sqlite3




app = Flask(__name__)
DATABASE = 'database.db'

# Comando para iniciar la app flask
# flask --app .\index.py run

@app.route("/")
def hello_world():
    return render_template('hello.html')


def get_db_connection():

    con = sqlite3.connect(DATABASE)
    # https://docs.python.org/3/library/sqlite3.html#how-to-create-and-use-row-factories
    con.row_factory = sqlite3.Row
    return con


@app.route('/products')
def item_list():
    with get_db_connection() as con:
        res = con.execute("SELECT * from products")
        items = res.fetchall()
    return render_template('products/list.html', items = items)
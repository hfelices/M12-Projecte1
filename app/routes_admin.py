from flask import Flask ,Blueprint, render_template, flash, redirect, url_for, request ,current_app
from flask_login import current_user, login_user, login_required, logout_user
from . import login_manager
from .models import User
from datetime import datetime
from .forms import LoginForm
from . import db_manager as db
from sqlalchemyseed import load_entities_from_json
from sqlalchemyseed import Seeder
from .forms import  CreateUserForm, LoginForm
from werkzeug.security import check_password_hash, generate_password_hash
from os import path
import csv
from io import TextIOWrapper
from . import db_manager as db
from .models import Product, Category, User, BlockedUser
from .helper_role import requireAdminRole, requireModeratePermission
from sqlalchemy.orm import aliased

basedir = path.abspath(path.dirname(__file__))


# Blueprint
admin_bp = Blueprint(
    "admin_bp", __name__, template_folder="templates", static_folder="static"
)

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
    blockedUsers = db.session.query(BlockedUser.user_id).all()
    blockedUsersId = list()
    for a in blockedUsers:
        blockedUsersId.append(a.user_id)

    return render_template('admin/users_list.html', users=users, blockedUsersId = blockedUsersId)

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


# BLOCK

@admin_bp.route('/admin/users/<int:id>/block', methods=["GET", "POST"])
@login_required
@requireAdminRole.require(http_exception=403)
def blockUser(id):
    user = User.query.get(id)
    if request.method == 'POST':
        
        blockedUser = BlockedUser()
        blockedUser.user_id = user.id
        blockedUser.message = "aloha"

        db.session.add(blockedUser)
        db.session.commit()
        return redirect(url_for('admin_bp.admin_users'))
    elif request.method == 'GET':
        return render_template ('admin/block.html')

#UNBLOCK
@admin_bp.route('/admin/users/<int:id>/unblock')
@login_required
@requireAdminRole.require(http_exception=403)
def unblockUser(id):
    user = BlockedUser.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin_bp.admin_users'))


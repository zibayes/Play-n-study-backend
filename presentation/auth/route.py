from flask_login import login_required, logout_user, login_user
from flask import Blueprint, redirect, render_template, request, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from logic.facade import LogicFacade
from presentation.UserLogin import UserLogin

engine = create_engine(
    'postgresql://postgres:postgres@localhost/postgres',
    echo=False
)
Session = sessionmaker(bind=engine)
session = Session()

logic = LogicFacade(session)

auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/logout")
@login_required
def handle_logout():
    logout_user()
    return render_template('index.html')


@auth_bp.route("/login", methods=['GET', 'POST'])
def handle_login():
    if request.method == 'POST':
        user = logic.user_auth(request.form['email'], request.form['password'])
        if user is None:
            flash('Неверный логин/пароль', 'error')
            return render_template('login.html')
        user_login = UserLogin().create(user)
        login_user(user_login)
        return redirect(f"/profiles/{user.user_id}")
    return render_template('login.html')


@auth_bp.route("/registration", methods=["POST", "GET"])
def handle_register():
    if request.method == 'POST':
        response = logic.user_register(request.form.copy())
        flash(*response)
    return render_template("registration.html")


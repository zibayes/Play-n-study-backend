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

chat_bp = Blueprint('auth', __name__)


@chat_bp.route("/")
@login_required
def handle_logout():
    logout_user()
    return render_template('index.html')

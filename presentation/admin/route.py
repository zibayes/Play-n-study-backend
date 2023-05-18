from flask_login import login_required, current_user
from flask import Blueprint, redirect, render_template, request, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data.types import User
from logic.facade import LogicFacade

engine = create_engine(
    'postgresql://postgres:postgres@localhost/postgres',
    echo=False
)
Session = sessionmaker(bind=engine)
session = Session()

logic = LogicFacade(session)

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin/add_curator', methods=["POST"])
@login_required
def handle_admin_add_curator():
    admin = logic.is_user_admin(current_user.get_id())
    if not admin:
        return "not allowed"
    user_id = int(request.form['user_id'])
    course_id = int(request.form['course_id'])
    response = logic.curator_add(user_id, course_id)
    if response:
        return "success"
    return "failure"


@admin_bp.route('/admin/remove_curator', methods=["POST"])
@login_required
def handle_admin_remove_curator():
    admin = logic.is_user_admin(current_user.get_id())
    if not admin:
        return "not allowed"
    user_id = int(request.form['user_id'])
    course_id = int(request.form['course_id'])
    response = logic.curator_remove(user_id, course_id)
    if response:
        return "success"
    return "failure"


from flask_login import login_required, current_user
from flask import Blueprint, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from access import check_access
from logic.facade import LogicFacade

engine = create_engine(
    'postgresql://postgres:postgres@localhost/postgres',
    echo=False
)
Session = sessionmaker(bind=engine)
session = Session()

logic = LogicFacade(session)

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/add_curator', methods=["POST"])
@login_required
@check_access(current_user, request)
def handle_admin_add_curator():
    user_id = int(request.form['user_id'])
    course_id = int(request.form['course_id'])
    response = logic.curator_add(user_id, course_id)
    if response:
        return "success"
    return "failure"


@admin_bp.route('/remove_curator', methods=["POST"])
@login_required
@check_access(current_user, request)
def handle_admin_remove_curator():
    user_id = int(request.form['user_id'])
    course_id = int(request.form['course_id'])
    response = logic.curator_remove(user_id, course_id)
    if response:
        return "success"
    return "failure"

from flask_login import login_required, current_user
from flask import Blueprint, redirect, render_template, request, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from logic.facade import LogicFacade

engine = create_engine(
    'postgresql://postgres:postgres@localhost/postgres',
    echo=False
)
Session = sessionmaker(bind=engine)
session = Session()

logic = LogicFacade(session)

api_bp = Blueprint('api', __name__)


@api_bp.route('/api/joincourse/<int:course_id>')
@login_required
def handle_join_course(course_id):
    response = logic.course_join(course_id, current_user.get_id())
    if response:
        return redirect(f'/course_preview/{course_id}')
    flash('Ошибка при подписке', 'error')


@api_bp.route('/api/leavecourse/<int:course_id>')
@login_required
def handle_join_leave_course(course_id):
    response = logic.course_leave(course_id, current_user.get_id())
    if response:
        return redirect(f'/course_preview/{course_id}')
    flash('Ошибка при отписке', 'error')
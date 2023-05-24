from markdown import markdown
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


@api_bp.route('/api/rendermd', methods=['POST'])
def handle_rendermd():
    return markdown(request.json['text'])


@api_bp.route('/api/set_rating/<int:course_id>', methods=['POST'])
@login_required
def handle_rate_course(course_id):
    user_id = current_user.get_id()
    reviews = logic.get_reviews_by_course_id(course_id)
    if reviews:
        for review in reviews:
            if review.user_id == user_id:
                response = logic.update_review(user_id, course_id, int(request.json['rate']))
                if response:
                    return "Спасибо за отзыв!"
                flash('Ошибка при отправке отзыва', 'error')
                return
    response = logic.add_review(user_id, course_id, int(request.json['rate']))
    if response:
        return "Спасибо за отзыв!"
    flash('Ошибка при отправке отзыва', 'error')

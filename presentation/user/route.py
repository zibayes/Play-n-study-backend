from flask_login import login_required, current_user
from flask import Blueprint, redirect, render_template, request, flash, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from logic.facade import LogicFacade
from data.types import Notification

engine = create_engine(
    'postgresql://postgres:postgres@localhost/postgres',
    echo=False
)
Session = sessionmaker(bind=engine)
session = Session()

logic = LogicFacade(session)

user_bp = Blueprint('user', __name__)


@user_bp.route('/subscribe/<int:user_id>')
@login_required
def handle_subscribe(user_id):
    response = logic.add_sub_relation(user_id, current_user.get_id())
    if response:
        username = logic.get_user_by_id(current_user.get_id()).username
        notif = Notification(None, user_id, 'Новый подписчик!',
                             'На вас подписался пользователь ' + username, '/profiles/' + str(current_user.get_id()), None, False)
        logic.add_notification(notif)
        return redirect(f"/profiles/{user_id}")
    else:
        flash('Ошибка при подписке', 'error')


@user_bp.route('/unsubscribe/<int:user_id>')
@login_required
def handle_unsubscribe(user_id):
    response = logic.remove_sub_relation(user_id, current_user.get_id())
    if response:
        return redirect(f"/profiles/{user_id}")
    else:
        flash('Ошибка при отписке', 'error')


@user_bp.route('/changecity', methods=['POST'])
@login_required
def handle_change_user_data():
    response = logic.change_user_data(request.form, current_user.get_id())
    return redirect('/settings')


@user_bp.route('/settings', methods=["GET"])
@login_required
def handle_settings():
    user = logic.get_user_by_id(current_user.get_id())
    return render_template('settings.html', user=user)


@user_bp.route('/uploadava', methods=["POST", "GET"])
@login_required
def handle_upload():
    if request.method == 'POST':
        logic.user_avatar_upload(request.files['file'], current_user)
    return redirect(url_for('user.handle_settings'))

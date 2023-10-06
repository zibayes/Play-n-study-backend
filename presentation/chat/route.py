from flask_login import login_required, logout_user, login_user, current_user
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

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/start_dialog/<int:user_id>', methods=['POST'])
def handle_start_chat(user_id):
    logic.chats_start_dialog(current_user.get_id(), user_id)
    return redirect(f'/messages')


@chat_bp.route('/get_chats', methods=['POST'])
def handle_get_chats():
    return logic.chats_get_user_chats_preview(current_user.get_id())


@chat_bp.route('/get_dialog', methods=['POST'])
def handle_get_chat_content():
    chat_id = int(request.json['chat_id'])
    return logic.chats_get_dialog(current_user.get_id(), chat_id)


@chat_bp.route('/send_message', methods=['POST'])
def handle_send_message():
    response = logic.chats_send_message(request.json, current_user.get_id())
    if response:
        return 'sent'
    return 'fail'


@chat_bp.route('/remove_message/<int:msg_id>', methods=['POST'])
def handle_send_message(msg_id):
    response = logic.remove_message(msg_id)
    if response:
        return 'removed'
    return 'fail'

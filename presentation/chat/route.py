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


@chat_bp.route('/get_chats', methods=['POST'])
def handle_get_chats():
    return logic.chats_get_user_chats_preview(current_user.get_id())


@chat_bp.route('/get_dialog', methods=['POST'])
def handle_get_chat_content():
    chat_id = int(request.json['chat_id'])
    return logic.chats_get_dialog(current_user.get_id(), chat_id)


@chat_bp.route('/send_message', methods=['POST'])
def handle_send_message():
    response = logic.chats_send_message(request.json, 1)
    if response:
        return 'sent'
    return 'fail'

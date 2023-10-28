from flask_login import login_required, current_user
from flask import Blueprint, redirect, render_template, request, flash, url_for
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

pages_bp = Blueprint('pages', __name__)


@pages_bp.route('/')
def handle_index():
    return render_template('index.html')


@pages_bp.route('/tasks')
def handle_task():
    user_id = current_user.get_id()
    user = logic.get_user_by_id(user_id)
    return render_template('tasks.html', user=user)


@pages_bp.route('/about')
def about():
    return "About"

@pages_bp.route('/messages')
def messages():
    user_id = current_user.get_id()
    user = logic.get_user_by_id(user_id)
    return render_template('messages.html', user=user)

@pages_bp.route('/profiles/<int:user_id>')
@login_required
def handle_profile(user_id):
    roles = logic.role_get_user_role_by_user_id(user_id)
    if roles:
        is_admin = 'admin' in roles
    else:
        is_admin = False
    user = logic.get_user_for_profile(user_id, current_user.get_id())
    return render_template("profile.html", user=user,
                           need_subscribe=user.need_subscribe, is_me=user.is_me, is_admin=is_admin)


@pages_bp.route('/add_admin/<int:user_id>')
@login_required
def handle_add_admin(user_id):
    logic.add_user_role_admin(user_id)
    return redirect(f'/profiles/{user_id}')


@pages_bp.route('/remove_admin/<int:user_id>')
@login_required
def handle_remove_admin(user_id):
    logic.remove_user_role_admin(user_id)
    return redirect(f'/profiles/{user_id}')


@login_required
@pages_bp.route('/subscriptions/<int:user_id>', methods=["POST", "GET"])
def handle_subscriptions(user_id):
    if request.method == "GET":
        user = logic.get_user_for_profile(user_id, current_user.get_id())
        return render_template('subscriptions.html', user=user, user_id=user_id)
    elif request.method == "POST":
        query = request.form['query']
        if len(query) > 0:
            found = logic.get_users_by_query(query)
            return render_template("subscriptions.html", user=User(), found=found, user_id=user_id)
    return render_template("subscriptions.html", user=User(), found=None, user_id=user_id)

@pages_bp.route('/forum')
def handle_forum_list():
    user_id = current_user.get_id()
    user = logic.get_user_by_id(user_id)
    return render_template('forum.html', user=user)
@pages_bp.route('/forum_list')
def handle_forum():
    user_id = current_user.get_id()
    user = logic.get_user_by_id(user_id)
    return render_template('forum_list.html', user=user)
@pages_bp.route('/reviews')
def handle_reviews():
    user = logic.get_user_by_id(current_user.get_id())
    return render_template('reviews_1.html', user=user)


@pages_bp.route('/information')
def handle_information():
    user = logic.get_user_by_id(current_user.get_id())
    print(request)
    return render_template('information.html', user=user)


@login_required
@pages_bp.route('/article_editor/<int:article_id>', methods=["GET"])
def handle_article_editor(article_id):
    user = logic.get_user_by_id(current_user.get_id())
    article = logic.article_get_by_id(article_id)
    return render_template('article_editor.html', user=user,
                           article=article)
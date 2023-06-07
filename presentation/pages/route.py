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


@pages_bp.route('/profiles/<int:user_id>')
@login_required
def handle_profile(user_id):
    user = logic.get_user_for_profile(user_id, current_user.get_id())
    return render_template("profile.html", user=user,
                           need_subscribe=user.need_subscribe, is_me=user.is_me)


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
from flask_login import login_required, current_user
from flask import Blueprint, redirect, render_template, request, flash, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.types import User
from logic.facade import LogicFacade
from presentation.auth.route import online_users

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


@pages_bp.route('/achievements/<int:user_id>')
@login_required
def handle_achievements(user_id):
    user = logic.get_user_by_id(user_id)
    achievements = logic.get_user_achievements(user_id)
    if achievements is None:
        achievements = []
    achs = []
    for ach in achievements:
        conditions = ach.condition.split(']][[')
        course_name = logic.get_course_without_rel(ach.course_id).name
        ach_to_add = {'ach_id': ach.ach_id, 'name': ach.name, 'description': ach.description, 'conditions': [],
                      'course_name': course_name, 'course_id': ach.course_id}
        for cond in conditions:
            condition = {}
            cond = cond.replace('[[', '').replace(']]', '')
            if 'score' in cond:
                condition['condition'] = 'score'
                cond = cond.replace('score', '')
                if ' > ' in cond:
                    condition['val_amount'] = '>'
                    cond = cond.replace(' > ', '')
                elif ' = ' in cond:
                    condition['val_amount'] = '='
                    cond = cond.replace(' = ', '')
                elif ' < ' in cond:
                    condition['val_amount'] = '<'
                    cond = cond.replace(' < ', '')
                condition['value'] = cond[:cond.find(' for ')]
                cond = cond[cond.find(' for '):]
            elif 'completion fact' in cond:
                condition['condition'] = 'completion fact'
            elif 'time spent' in cond:
                condition['condition'] = 'time spent'
                cond = cond.replace('time spent', '')
                condition['time'] = cond[:cond.find(' for ')]
                cond = cond[cond.find(' for '):]
            cond = cond.replace(condition['condition'], '')
            if 'tasks' in cond:
                condition['task_category'] = 'tasks'
                cond = cond.replace(' for tasks:', '')
            elif 'units' in cond:
                condition['task_category'] = 'units'
                cond = cond.replace(' for units:', '')
            condition['tasks'] = []
            for task in cond.split(';'):
                if task != ' ':
                    condition['tasks'].append(task)
            ach_to_add['conditions'].append(condition)
        achs.append(ach_to_add)
    return render_template('achievements.html', user=user, achievements=achs)


@pages_bp.route('/profiles/<int:user_id>')
@login_required
def handle_profile(user_id):
    roles = logic.role_get_user_role_by_user_id(user_id)
    if roles:
        is_admin = 'admin' in roles
    else:
        is_admin = False
    user_to_show = logic.get_user_for_profile(user_id, current_user.get_id())
    user = logic.get_user_by_id(current_user.get_id())
    return render_template("profile.html", user=user, user_to_show=user_to_show, online_users=online_users,
                           need_subscribe=user_to_show.need_subscribe, is_me=user_to_show.is_me, is_admin=is_admin)


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
        return render_template('subscriptions.html', user=user, online_users=online_users, user_id=user_id)
    elif request.method == "POST":
        query = request.form['query']
        if len(query) > 0:
            found = logic.get_users_by_query(query)
            return render_template("subscriptions.html", user=User(), found=found, online_users=online_users, user_id=user_id)
    return render_template("subscriptions.html", user=User(), found=None, online_users=online_users, user_id=user_id)


@login_required
@pages_bp.route('/subscribers/<int:user_id>', methods=["POST", "GET"])
def handle_subscribers(user_id):
    if request.method == "GET":
        user = logic.get_user_for_profile(user_id, current_user.get_id())
        return render_template('subscribers.html', user=user, online_users=online_users, user_id=user_id)
    elif request.method == "POST":
        query = request.form['query']
        if len(query) > 0:
            found = logic.get_users_by_query(query)
            return render_template("subscribers.html", user=User(), online_users=online_users, found=found, user_id=user_id)
    return render_template("subscribers.html", user=User(), online_users=online_users, found=None, user_id=user_id)


@pages_bp.route('/reviews')
def handle_reviews():
    user = logic.get_user_by_id(current_user.get_id())
    return render_template('reviews_1.html', user=user)


@pages_bp.route('/information')
def handle_information():
    user = logic.get_user_by_id(current_user.get_id())
    print(request)
    return render_template('information.html', user=user)


@pages_bp.route('/remove_notification/<int:notif_id>', methods=['POST'])
def handle_remove_notification(notif_id):
    response = logic.remove_notification(notif_id)
    if response:
        return 'notification removed'
    return 'notification remove failed'


@pages_bp.route('/remove_all_notifications/<int:user_id>', methods=['POST'])
def handle_remove_all_notifications(user_id):
    response = logic.remove_all_notifications_by_user_id(user_id)
    if response:
        return 'notifications removed'
    return 'notifications remove failed'


@pages_bp.route('/read_notifications/<int:user_id>', methods=['POST'])
def handle_read_notifications(user_id):
    notifications = logic.get_all_notifications_by_user_id(user_id)
    if notifications:
        for notif in notifications:
            notif.user_to_read = True
            response = logic.update_notification(notif)
            if not response:
                return 'notifications read failed'
    return 'notifications read'
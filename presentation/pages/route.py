from flask_login import login_required, current_user
from flask import Blueprint, redirect, render_template, request, flash, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.types import User, Note, Deadline
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


@login_required
@pages_bp.route('/tasks')
def handle_task():
    user_id = current_user.get_id()
    user = logic.get_user_by_id(user_id)
    notes = logic.get_all_notes_by_user_id(user_id)
    deadlines = logic.get_all_deadlines_by_user_id(user_id)
    return render_template('tasks.html', user=user, notes=notes, deadlines=deadlines, calendar=False)


@login_required
@pages_bp.route('/calendar')
def handle_calendar():
    user_id = current_user.get_id()
    user = logic.get_user_by_id(user_id)
    notes = logic.get_all_notes_by_user_id(user_id)
    deadlines = logic.get_all_deadlines_by_user_id(user_id)
    return render_template('tasks.html', user=user, notes=notes, deadlines=deadlines, calendar=True)


@login_required
@pages_bp.route('/add_deadline', methods=['POST'])
def handle_add_deadline():
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    if not start_date:
        start_date = None
    if not end_date:
        end_date = None
    deadline = Deadline(None, None, None, None, current_user.get_id(), request.form['title'], start_date, end_date)
    logic.add_deadline(deadline)
    return redirect(url_for('pages.handle_calendar'))


@login_required
@pages_bp.route('/edit_deadline/<int:deadline_id>', methods=['POST'])
def handle_edit_deadline(deadline_id):
    deadline = logic.get_deadline_by_id(deadline_id)
    deadline.title = request.form['title']
    if not request.form['start_date']:
        deadline.start_date = request.form['end_date']
        deadline.end_date = None
    elif not request.form['end_date']:
        deadline.start_date = request.form['start_date']
        deadline.end_date = None
    else:
        deadline.start_date = request.form['start_date']
        deadline.end_date = request.form['end_date']
    logic.update_deadline(deadline)
    return redirect(url_for('pages.handle_calendar'))


@login_required
@pages_bp.route('/remove_deadline/<int:deadline_id>', methods=['GET'])
def handle_remove_deadline(deadline_id):
    logic.remove_deadline(deadline_id)
    return redirect(url_for('pages.handle_calendar'))


@login_required
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


@login_required
@pages_bp.route('/reviews')
def handle_reviews():
    site_id = 0
    user = logic.get_user_by_id(current_user.get_id())
    reviews = logic.get_reviews_by_course_id(site_id)
    user_review = None
    users_for_review = {}
    if reviews:
        for review in reviews:
            if review.user_id == user.user_id:
                user_review = review
            users_for_review[review.user_id] = logic.get_user_by_id(review.user_id)
    else:
        reviews = []
    return render_template('site_reviews.html', user=user, reviews=reviews, user_review=user_review, site_id=site_id,
                           users_for_review=users_for_review)


@login_required
@pages_bp.route('/information')
def handle_information():
    user = logic.get_user_by_id(current_user.get_id())
    print(request)
    return render_template('information.html', user=user)


@login_required
@pages_bp.route('/remove_notification/<int:notif_id>', methods=['POST'])
def handle_remove_notification(notif_id):
    response = logic.remove_notification(notif_id)
    if response:
        return 'notification removed'
    return 'notification remove failed'


@login_required
@pages_bp.route('/remove_all_notifications/<int:user_id>', methods=['POST'])
def handle_remove_all_notifications(user_id):
    response = logic.remove_all_notifications_by_user_id(user_id)
    if response:
        return 'notifications removed'
    return 'notifications remove failed'


@login_required
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


@login_required
@pages_bp.route('/add_note', methods=['POST'])
def handle_add_note():
    note = Note(None, current_user.get_id(), request.json['title'], request.json['text'], None)
    response = logic.add_note(note)
    if response:
        return str(logic.get_last_note().note_id)
    return 'add note failed'


@login_required
@pages_bp.route('/remove_note/<int:note_id>', methods=['POST'])
def handle_remove_note(note_id):
    response = logic.remove_note(note_id)
    if response:
        return 'note removed'
    return 'note remove failed'


@login_required
@pages_bp.route('/update_note/<int:note_id>', methods=['POST'])
def handle_update_note(note_id):
    note = logic.get_note_by_id(note_id)
    note.note_text = request.json['text']
    note.note_title = request.json['title']
    response = logic.update_note(note)
    if response:
        return 'note updated'
    return 'note update failed'

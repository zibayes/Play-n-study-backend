from sqlalchemy import create_engine
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy.orm import sessionmaker
from werkzeug.security import check_password_hash
from flask_login import LoginManager, login_user, login_required
from infrastructure.auth.UserLogin import UserLogin
from infrastructure.auth.service import get_register_wrong_field_msg, get_fields_for_register
from infrastructure.QueryManager import *
from infrastructure.repository.AchievementRepository import AchievementRepository
from infrastructure.repository.UserRepository import UserRepository
from infrastructure.repository.AchieveRelRepository import AchieveRelRepository


engine = create_engine(
    'postgresql://postgres:postgres@localhost/postgres',
    echo=False
)
Session = sessionmaker(bind=engine)
session = Session()

print(session)

app = Flask(__name__)
app.secret_key = 'super secret key'
login_manager = LoginManager(app)


# Repositories
user_repository = UserRepository(session)
achieve_rel_repository = AchieveRelRepository(session)
achievement_repository = AchievementRepository(session)
course_repository = CourseRepository(session)
course_rel_repository = CourseRelRepository(session)
curator_repository = CuratorRepository(session)
review_repository = ReviewRepository(session)
task_repository = TaskRepository(session)

# QueryManager
query_manager = QueryManager(user_repository=user_repository,
                             achievement_repository=achievement_repository,
                             achieve_rel_repository=achieve_rel_repository,
                             course_repository=course_repository,
                             course_rel_repository=course_rel_repository,
                             curator_repository=curator_repository,
                             review_repository=review_repository,
                             task_repository=task_repository)


@login_manager.user_loader
def load_user(user_id):
    print('load_user')
    return UserLogin().from_db(user_repository, user_id)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return "About"


@app.route('/profiles/<int:user_id>')
@login_required
def handle_profile(user_id):
    user = user_repository.get_user_by_id(user_id)
    user.achievements = query_manager.get_user_achievements(user.user_id)
    json_response = {}

    i = 0
    for ach in user.achievements:
        json_response[i] = {
            "name": ach.name,
            "image": ach.image
        }
        i += 1
    return json_response


@app.route("/login", methods=['GET', 'POST'])
def handle_login():
    if request.method == 'POST':
        user = user_repository.get_user_by_email(request.form['email'])

        if user is not None and check_password_hash(user.password, request.form['password']):
            user_login = UserLogin().create(user)
            login_user(user_login)
            return redirect(url_for('handle_main'))
        flash('Неверный логин/пароль', 'error')

    return render_template('login.html')


@app.route("/registration", methods=["POST", "GET"])
def handle_register():
    # Ссылки для перенаправления в случае неудачной/удачной регистрации
    current_template = url_for('handle_register').replace('/', '') + '.html'
    login_url = url_for('handle_login')

    form_data = request.form.copy()
    if request.method == 'POST':
        # Получаем либо сообщение об ошибке, либо None если все ОК
        error = get_register_wrong_field_msg(session, form_data)
        if error is None:
            if user_repository.add_user(*get_fields_for_register(form_data)):
                flash('Вы успешно зарегистрированы', 'success')
                return redirect(login_url)
            flash('Ошибка при add_user', 'error')
        else:
            flash(error, 'error')
    return render_template(current_template)


@app.route('/main')
def handle_main():
    return render_template('main.html')


@app.route('/profile')
def handle_settings():
    return render_template('profile.html')


@app.route('/reviews')
def handle_reviews():
    return render_template('reviews.html')


@app.route('/schedule')
def handle_schedule():
    return render_template('schedule.html')


@app.route('/information')
def handle_information():
    return render_template('information.html')


class Bunch:
    pass


@app.route('/settings')
def open_profile():
    user = Bunch()
    user.name = 'Эрнесто'
    user.surname = 'Че Гевара'
    user.phone = '88005553535'
    user.email = 'Ernesto@gmail.com'
    user.city = 'Красноярск'
    user.university = 'ИКИТ СФУ'
    user.specialization = '09.03.04 Программная инженерия'
    user.group = 'КИ20-16/2Б'
    return render_template('settings.html', user = user)


if __name__ == "__main__":
    app.run(debug=True)

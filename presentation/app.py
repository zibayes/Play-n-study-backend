from sqlalchemy import create_engine
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy.orm import sessionmaker
from presentation.models.models import *
from werkzeug.security import check_password_hash
from infrastructure.repository.UserRepository import UserRepository
from flask_login import LoginManager, login_user, login_required
from infrastructure.auth.UserLogin import UserLogin
from infrastructure.auth.service import get_register_wrong_field_msg, get_fields_for_register
from infrastructure.user.queries import *
engine = create_engine(
    'postgresql://postgres:postgres@localhost/postgres',
    echo=False
)
Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)
app.secret_key = 'super secret key'
login_manager = LoginManager(app)


# Repositories
user_repository = UserRepository(session)


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
    print(user.json())
    return render_template('profile.html', context=user.json())

#
# @app.route('/profile/<int:user_id>/courses')
# def handle_get_user_courses(user_id):
#     courses = session.query(UsersModel, CoursesModel, CoursesRelModel) \
#         .filter(CoursesRelModel.user_id == UsersModel.user_id) \
#         .filter(CoursesRelModel.course_id == CoursesModel.course_id) \
#         .filter(UsersModel.user_id == user_id).all()
#
#     result = {"total": len(courses)}
#
#     i = 0
#     for row in courses:
#         course = row[1].name
#         temp = {'course_name': course}
#         result[f"{i}"] = temp
#         i += 1
#     return result


@app.route("/login", methods=['GET', 'POST'])
def handle_login():
    #
    current_template = url_for('handle_login').replace('/', '') + '.html'

    if request.method == 'POST':
        user = user_repository.get_user_by_email(request.form['email'])

        if user is not None and check_password_hash(user.password, request.form['password']):
            user_login = UserLogin().create(user)
            login_user(user_login)
            return redirect(url_for('index'))
        flash('Неверный логин/пароль', 'error')

    return render_template(current_template)


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


if __name__ == "__main__":
    app.run(debug=True)

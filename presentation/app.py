from sqlalchemy import create_engine
from flask import Flask, make_response, render_template
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager, login_required
from logic.facade import LogicFacade
from presentation.UserLogin import UserLogin

# blueprints
from presentation.courses.route import courses_bp as courses
from presentation.admin.route import admin_bp as admin
from presentation.user.route import user_bp as user
from presentation.pages.route import pages_bp as pages
from presentation.api.route import api_bp as api
from presentation.auth.route import auth_bp as auth
engine = create_engine(
    'postgresql://postgres:postgres@localhost/postgres',
    echo=False
)
Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)
app.secret_key = 'super secret key'
app.register_blueprint(courses)
app.register_blueprint(admin)
app.register_blueprint(api)
app.register_blueprint(pages)
app.register_blueprint(user)
app.register_blueprint(auth)

# login manager
login_manager = LoginManager(app)

# logic layer instance
logic = LogicFacade(session)


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().from_db(logic, user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return render_template('index.html')


@app.route('/courseava/<int:course_id>')
@login_required
def handle_course_ava(course_id):
    img = logic.course_get_avatar(app, course_id)
    if not img:
        return ""
    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@app.route('/userava/<int:user_id>')
def handle_userava(user_id):
    img = logic.get_user_avatar(app, user_id)
    if not img:
        return ""
    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


if __name__ == "__main__":
    app.run(debug=True)
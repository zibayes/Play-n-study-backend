from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask, render_template, url_for, request
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, ARRAY, String, Text, JSON, Date, Boolean
from sqlalchemy import Table, Column, ForeignKey

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost/postgres"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class UsersModel(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(40), unique=True)
    city = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(128), nullable=False)
    courses = Column(ARRAY(Integer))

    def __init__(self, email, city, username, password, courses):
        self.email = email
        self.city = city
        self.username = username
        self.password = password
        self.courses = courses

    def __repr__(self):
        return "<User %r>" % self.id


class CoursesModel(db.Model):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    course = Column(Text, nullable=False)

    def __init__(self, course):
        self.course = course

    def __repr__(self):
        return "<Course %r"


class CuratorsModel(db.Model):
    __tablename__ = "curators"

    id = Column(Integer, primary_key=True)
    email = Column(String(40), ForeignKey("users.email"))
    course = Column(Integer, ForeignKey("courses.id"))

    def __init__(self, email, course):
        self.email = email
        self.course = course

    def __repr__(self):
        return ""


class AchievementsModel(db.Model):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    image = Column(Text)
    course = Column(Integer, ForeignKey("courses.id"))
    email = Column(String(40), ForeignKey("users.email"))

    def __init__(self, name, image, course, email):
        self.name = name
        self.image = image
        self.course = course
        self.email = email

    def __repr__(self):
        return "<Achievement %r>" % self.id


class TasksModel(db.Model):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    task = Column(Text, nullable=False)
    tags = Column(ARRAY(Text))
    description = Column(Text)
    attachments = Column(JSON)
    date = Column(Date, nullable=False)
    completed = Column(Boolean)
    email = Column(String(40), ForeignKey("users.email"))

    def __init__(self, task, tags, description, attachments, date, completed, email):
        self.task = task
        self.tags = tags
        self.description = description
        self.attachments = attachments
        self.date = date
        self.completed = completed
        self.email = email

    def __repr__(self):
        return "<Task %r>" % self.id


# USERS CRUD

# USERS CREATE
@app.route('/api/createUser', methods=['POST'])
def handle_add_user():
    if request.is_json:
        data = request.get_json()
        new_user = UsersModel(
            email=data['email'],
            city=data['city'],
            username=data['username'],
            password=data['password'],
            courses=data['courses']
        )
        db.session.add(new_user)
        db.session.commit()
        return {"message": f"user {new_user.username} has been created successfully."}
    else:
        return {"error": "The request payload is not in JSON format"}


# USERS READ
@app.route('/users', methods=['GET'])
def handle_users():
    users = UsersModel.query.all()
    results = [
        {
            "username": user.username
        } for user in users]
    return {"count": len(results), "users": results}


# USERS UPDATE
@app.route('/api/updateUser', methods=['POST'])
def handle_update_user():
    if request.is_json:
        data = request.get_json()
        user_id = data['user_id']

        user = UsersModel.query.get_or_404(user_id)

        user.email = data['email']
        user.city = data['city']
        user.username = data['username']
        user.password = data['password']
        user.courses = data['courses']

        db.session.add(user)
        db.session.commit()

        return {"message": f"user {user.name} successfully updated"}
    else:
        return {"error": "The request payload is not in JSON format"}


# USERS DELETE
@app.route('/api/deleteUser', methods=['POST'])
def handle_delete_user():
    if request.is_json:

        data = request.get_json()
        user_id = data['user_id']

        user = UsersModel.query.get_or_404(user_id)

        db.session.delete(user)
        db.session.commit()
        return {"message": f"User {user.name} successfully deleted."}
    else:
        return {"error": "The request payload is not in JSON format"}


####################

# COURSES CRUD

# COURSES CREATE
@app.route('/api/createCourse', methods=['POST'])
def handle_add_course():
    if request.is_json:
        data = request.get_json()
        new_course = CoursesModel(
            course=data['course']
        )
        db.session.add(new_course)
        db.session.commit()
        return {"message": f"Course {new_course.course} has been created successfully."}
    else:
        return {"error": "The request payload is not in JSON format"}


# COURSES READ
@app.route('/courses', methods=['GET'])
def handle_courses():
    courses = CoursesModel.query.all()
    results = [
        {
            "course": course.course
        } for course in courses]
    return {"count": len(results), "courses": results}


# COURSES UPDATE
@app.route('/api/updateCourse', methods=['POST'])
def handle_update_course(course_id):
    if request.is_json:
        course = CoursesModel.query.get_or_404(course_id)

        data = request.get_json()
        course.course = data['course']

        db.session.add(course)
        db.session.commit()
        return {"message": f"Course {course.name} successfully updated"}
    else:
        return {"error": "The request payload is not in JSON format"}


# COURSES DELETE
@app.route('/api/deleteCourse', methods=['POST'])
def handle_delete_course(course_id):
    course = CoursesModel.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return {"message": f"Course {course.name} successfully deleted."}


####################

# CURATORS CRUD

# CURATORS CREATE
@app.route('/api/createCurator')
def handle_create_curator():
    if request.is_json:
        data = request.get_json()
        new_curator = CuratorsModel(
            email=data['email'],
            course=data['course']
        )
        db.session.add(new_curator)
        db.session.commit()
        return {"message": f"Curator {new_curator.email} has been created successfully."}
    else:
        return {"error": "The request payload is not in JSON format"}


# CURATORS READ
@app.route('/curators', methods=['GET'])
def handle_curators():
    curators = CuratorsModel.query.all()
    results = [
        {
            "curator": curator.email
        } for curator in curators]
    return {"count": len(results), "curators": results}


# CURATORS UPDATE
@app.route('/api/updateCurator')
def handle_update_curator(curator_id):
    if request.is_json:
        curator = CuratorsModel.query.get_or_404(curator_id)

        data = request.get_json()
        curator.email = data['email']
        curator.course = data['course']

        db.session.add(curator)
        db.session.commit()

        return {"message": f"curator {curator.email} successfully updated"}
    else:
        return {"error": "The request payload is not in JSON format"}


# CURATORS DELETE
@app.route('/api/deleteCurator')
def handle_delete_curator(curator_id):
    curator = CuratorsModel.query.get_or_404(curator_id)
    db.session.delete(curator)
    db.session.commit()
    return {"message": f"Curator {curator.email} successfully deleted."}


####################

# ACHIEVEMENTS CRUD

# ACHIEVEMENTS CREATE
@app.route('/api/create', methods=['POST'])
def handle_create_achievement():
    if request.is_json:
        data = request.get_json()
        new_achievement = AchievementsModel(
            name=data['name'],
            image=data['image'],
            course=data['course'],
            email=data['email']
        )
        db.session.add(new_achievement)
        db.session.commit()
        return {"message": f"Achievement {new_achievement.name} has been created successfully."}
    else:
        return {"error": "The request payload is not in JSON format"}


# ACHIEVEMENTS READ
@app.route('/achievements', methods=['GET'])
def handle_achievements():
    achievements = AchievementsModel.query.all()
    results = [
        {
            "achievement": achievement.name
        } for achievement in achievements]
    return {"count": len(results), "achievements": results}


# ACHIEVEMENTS UPDATE
@app.route('/api/updateAchievement', methods=['POST'])
def handle_update_achievement(achievement_id):
    if request.is_json:
        achievement = AchievementsModel.query.get_or_404()

        data = request.get_json()
        achievement.name = data['name']
        achievement.image = data['image']
        achievement.course = data['course']
        achievement.email=data['email']

        db.session.add(achievement)
        db.session.commit()

        return {"message": f"Achievement {achievement.name} successfully updated"}
    else:
        return {"error": "The request payload is not in JSON format"}


# ACHIEVEMENT DELETE
@app.route('/api/deleteAchievement')
def handle_delete_achievement(achievement_id):
    achievement = AchievementsModel.query.get_or_404(achievement_id)
    db.session.delete(achievement)
    db.session.commit()
    return {"message": f"Achievement {achievement.name} successfully deleted."}


####################

# TASKS CRUD

# TASK CREATE
@app.route('/api/createTask')
def handle_create_task():
    if request.is_json:
        data = request.get_json()
        new_task = TasksModel(
            task=data['task'],
            tags=data['tags'],
            description=data['description'],
            attachments=data['attachments'],
            date=data['date'],
            completed=data['completed'],
            email=data['email']
        )
        db.session.add(new_task)
        db.session.commit()
        return {"message": f"Curator {new_task.task} has been created successfully."}
    else:
        return {"error": "The request payload is not in JSON format"}


# TASKS READ
@app.route('/tasks')
def handle_tasks():
    tasks = TasksModel.query.all()
    results = [
        {
            "name": task.task
        } for task in tasks]
    return {"count": len(results), "tasks": results}


# TASKS UPDATE
@app.route('/api/updateUser', methods=['POST'])
def handle_update_task(task_id):
    if request.is_json:
        task = TasksModel.query.get_or_404(task_id)

        data = request.get_json()
        task.task = data['task']
        task.tags = data['tags']
        task.description = data['description']
        task.attachments = data['attachments']
        task.date = data['date']
        task.completed = data['completed']
        task.email = data['email']

        db.session.add(task)
        db.session.commit()

        return {"message": f"Task {task.name} successfully updated"}
    else:
        return {"error": "The request payload is not in JSON format"}


# TASKS DELETE
@app.route('/api/deleteTask', methods=['POST'])
def handle_delete_task(task_id):
    task = UsersModel.query.get_or_404(task_id)

    db.session.delete(task)
    db.session.commit()

    return {"message": f"Task {task.task} successfully deleted."}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return "About"


@app.route('/profile/<int:id>')
def handle_profile(id):
    user = UsersModel.query.filter_by(id=id).first_or_404()
    result = {
                "email": user.email,
                "city": user.city,
                "username": user.username,
                "courses": user.courses
            }
    return {"user": result}


if __name__ == "__main__":
    app.run(debug=True)

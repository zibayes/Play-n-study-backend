from sqlalchemy import create_engine, update, select, insert, delete
from flask import Flask, render_template, request
from sqlalchemy.orm import sessionmaker
from models import UsersModel, TasksModel, AchieveRelModel, \
    CoursesModel, CuratorsModel, AchievementsModel, CoursesRelModel

engine = create_engine(
    'postgresql://postgres:postgres@localhost/postgres',
    echo=False
)
Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)


# USERS
@app.route('/api/users', methods=['GET'])
def handle_users():
    users = session.query(UsersModel).all()
    results = [
        {
            "username": user.username,
            "city": user.city
        } for user in users]
    return {"count": len(results), "users": results}


@app.route('/api/users', methods=['POST'])
def handle_add_user():
    if request.is_json:
        data = request.get_json()
        new_user = UsersModel(
            email=data['email'],
            city=data['city'],
            username=data['username'],
            password=data['password']
        )
        session.add(new_user)
        session.commit()
        return {"message": f"user {new_user.username} has been created successfully."}
    else:
        return {"error": "The request payload is not in JSON format"}


@app.route('/api/users', methods=['PUT'])
def handle_update_user():
    if request.is_json:
        data = request.get_json()

        user = session.query(UsersModel) \
            .filter_by(user_id=data['user_id']) \
            .first()

        user.email = data['email']
        user.city = data['city']
        user.username = data['username']
        user.password = data['password']
        user.courses = data['courses']

        session.add(user)

        return {"message": f"user {user.id} successfully updated"}
    else:
        return {"error": "The request payload is not in JSON format"}


# USERS DELETE
@app.route('/api/deleteUser', methods=['DELETE'])
def handle_delete_user():
    if request.is_json:

        data = request.get_json()
        user_id = data['user_id']

        user = session.query(UsersModel) \
            .filter_by(user_id=data['user_id']) \
            .first()

        session.delete(user)
        session.commit()
        return {"message": f"User {user.id} successfully deleted."}
    else:
        return {"error": "The request payload is not in JSON format"}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return "About"


@app.route('/profile/<int:id>')
def handle_profile(id):
    user = session.query(UsersModel) \
        .filter_by(user_id=id) \
        .first()
    result = {
        "email": user.email,
        "city": user.city,
        "username": user.username,
    }
    return {"user": result}


# def test_query():
#     conn = engine.connect()
#     query = select([StudentsModel, MarksModel, SubjectsModel, GroupsModel])\
#         .where(MarksModel.stud_id == StudentsModel.stud_id)\
#         .where(SubjectsModel.subject_id == MarksModel.subject_id)\
#         .where(GroupsModel.group_id == StudentsModel.group_id)\
#         .where(MarksModel.value == 5)
#
#     return conn.execute(query)


@app.route('/api/getUserAchievements', methods=["POST"])
def handle_get_user_achievements():
    if request.is_json:

        data = request.get_json()

        conn = engine.connect()
        query = select([UsersModel, AchievementsModel, AchieveRelModel, CoursesModel]) \
            .where(UsersModel.user_id == AchieveRelModel.user_id) \
            .where(AchievementsModel.ach_id == AchieveRelModel.ach_id) \
            .where(AchievementsModel.course_id == CoursesModel.course_id) \
            .where(UsersModel.user_id == data['user_id'])
        res = conn.execute(query)

        result = {"total": res.rowcount}
        i = 0
        for row in res:
            ach = row[7]
            name = row[13]
            temp = {'name': ach, 'course_name': name}
            result[f"{i}"] = temp
            i += 1
        return result
    else:
        return {"error": "The request payload is not in JSON format"}


if __name__ == "__main__":
    app.run(debug=True)

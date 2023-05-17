from sqlalchemy.types import Integer, ARRAY, String, Text, Date, Boolean, JSON
from sqlalchemy import Column, ForeignKey, CheckConstraint, LargeBinary
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class UsersModel(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    email = Column(Text, unique=True, nullable=False)
    username = Column(Text, unique=True, nullable=False)
    city = Column(Text, nullable=False)
    avatar = Column(LargeBinary, nullable=True, default=None)
    password = Column(Text, nullable=False)

    # relationships
    tasks = relationship("TasksModel", back_populates="user")
    curator = relationship("CuratorsModel", back_populates="user")
    courses_rel = relationship("CoursesRelModel", back_populates="user")
    achieve_rel = relationship("AchieveRelModel", back_populates="user")
    reviews = relationship("ReviewsModel", back_populates="user")

    def __init__(self, email, city, username, password):
        self.email = email
        self.city = city
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User user_id={self.user_id}> " \
               f"email='{self.email}' " \
               f"username='{self.username}' " \
               f"city='{self.city}'>"


class CoursesModel(Base):
    __tablename__ = "courses"

    course_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    avatar = Column(LargeBinary)
    description = Column(Text)
    category = Column(Text)
    content = Column(JSON)

    # relationships
    curators = relationship("CuratorsModel", back_populates="course")
    courses_rel = relationship("CoursesRelModel", back_populates="course")
    achievements = relationship("AchievementsModel", back_populates="course")
    reviews = relationship("ReviewsModel", back_populates="course")

    def __init__(self, name, avatar, description, category, content):
        self.name = name
        self.avatar = avatar
        self.description = description
        self.category = category
        self.content = content

    def __repr__(self):
        return f"<Course course_id={self.course_id} " \
               f"name='{self.name}'>"


class CuratorsModel(Base):
    __tablename__ = "curators"

    cur_rel_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    course_id = Column(Integer, ForeignKey("courses.course_id"))

    # relationships
    user = relationship("UsersModel", back_populates="curator")
    course = relationship("CoursesModel", back_populates="curators")

    def __init__(self, user_id, course_id):
        self.user_id = user_id
        self.course_id = course_id

    def __repr__(self):
        return f"<Curator rel user_id={self.user_id} " \
               f"course_id={self.course_id}>"


class AchievementsModel(Base):
    __tablename__ = "achievements"

    ach_id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.course_id"))
    name = Column(Text, nullable=False, unique=True)
    image = Column(Text)

    # relationships
    course = relationship("CoursesModel", back_populates="achievements")
    achieve_rel = relationship("AchieveRelModel", back_populates="achievement")

    def __init__(self, course_id, name, image):
        self.course_id = course_id
        self.name = name
        self.image = image

    def __repr__(self):
        return f"<Achievement ach_id={self.ach_id} " \
               f"name='{self.name}' " \
               f"image='{self.image}'>"


class TasksModel(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    name = Column(Text, nullable=False)
    tags = Column(ARRAY(Text))
    description = Column(Text)
    date = Column(Date, nullable=False)
    completed = Column(Boolean)

    # relationships
    user = relationship("UsersModel", back_populates="tasks")

    def __init__(self, user_id, name, tags, description, date, completed):
        self.user_id = user_id
        self.name = name
        self.tags = tags
        self.description = description
        self.date = date
        self.completed = completed

    def __repr__(self):
        return f"<Task task_id={self.task_id} " \
               f"user_ud={self.user_id} " \
               f"name='{self.name}' " \
               f"tags={self.tags} " \
               f"description='{self.description}' " \
               f"date={self.date} " \
               f"completed={self.completed}>"


class AchieveRelModel(Base):
    __tablename__ = "achieve_rel"

    ach_rel_id = Column(Integer, primary_key=True)
    ach_id = Column(Integer, ForeignKey("achievements.ach_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))

    # relationships
    user = relationship("UsersModel", back_populates="achieve_rel")
    achievement = relationship("AchievementsModel", back_populates="achieve_rel")

    def __init__(self, ach_id, user_id):
        self.ach_id = ach_id
        self.user_id = user_id

    def __repr__(self):
        return f"<Achieve Rel ach_id={self.ach_id} " \
               f"user_id={self.user_id}>"


class CoursesRelModel(Base):
    __tablename__ = "courses_rel"

    cour_rel_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    course_id = Column(Integer, ForeignKey("courses.course_id"))

    # relationships
    user = relationship("UsersModel", back_populates="courses_rel")
    course = relationship("CoursesModel", back_populates="courses_rel")

    def __init__(self, user_id, course_id):
        self.user_id = user_id
        self.course_id = course_id

    def __repr__(self):
        return f"<Course Rel user_id={self.user_id} " \
               f"course_id={self.course_id}>"


class ReviewsModel(Base):
    __tablename__ = "reviews"

    __table_args__ = (
        CheckConstraint('rate > 0'),
        CheckConstraint('rate < 11')
    )

    rev_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    course_id = Column(Integer, ForeignKey("courses.course_id"))
    rate = Column(Integer, nullable=False)
    text = Column(Text)

    # relationships
    user = relationship("UsersModel", back_populates="reviews")
    course = relationship("CoursesModel", back_populates="reviews")

    def __init__(self, user_id, course_id, rate, text=""):
        self.user_id = user_id
        self.course_id = course_id
        self.rate = rate
        self.text = text

    def __repr__(self):
        return f"<Review user_id={self.user_id} " \
               f"course_id={self.course_id}> " \
               f"rate={self.rate} " \
               f"text='{self.text}'"


class SubRelModel(Base):
    __tablename__ = 'sub_rel'

    sub_rel_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    sub_id = Column(Integer, ForeignKey("users.user_id"))

    def __init__(self, user_id, sub_id):
        self.user_id = user_id
        self.sub_id = sub_id

    # __repr__ impl


class TestsModel(Base):
    __tablename__ = 'tests'
    test_id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.course_id"))
    content = Column(JSON)

    def __init__(self, course_id, content):
        self.course_id = course_id
        self.content = content

    # __repr__ impl


class ArticlesModel(Base):
    __tablename__ = 'articles'
    article_id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.course_id"))
    content = Column(Text)

    def __init__(self, course_id, content):
        self.course_id = course_id
        self.content = content


class UsersProgressModel(Base):
    __tablename__ = "users_progress"

    up_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    course_id = Column(Integer, ForeignKey("courses.course_id"))
    progress = Column(JSON)

    def __init__(self, user_id, course_id, progress):
        self.user_id = user_id
        self.course_id = course_id
        self.progress = progress


class RolesModel(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True)
    name = Column(Text)

    def __init__(self, name):
        self.name = name


class UsersRolesModel(Base):
    __tablename__ = "users_roles"

    ur_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    role_id = Column(Integer, ForeignKey("roles.role_id"))

    def __init__(self, user_id, role_id):
        self.user_id = user_id
        self.role_id = role_id

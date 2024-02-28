-- DROP TABLE  notes CASCADE;
-- DROP TABLE  notifications CASCADE;
-- DROP TABLE  users_progress CASCADE;
-- DROP TABLE  topic_messages CASCADE;
-- DROP TABLE  forum_topics CASCADE;
-- DROP TABLE  forums CASCADE;
-- DROP TABLE  articles CASCADE ;
-- DROP TABLE  links CASCADE;
-- DROP TABLE  tests CASCADE;
-- DROP TABLE  sub_rel CASCADE;
-- DROP TABLE  reviews CASCADE;
-- DROP TABLE  courses_rel CASCADE;
-- DROP TABLE  achieve_rel CASCADE;
-- DROP TABLE  tasks CASCADE;
-- DROP TABLE  achievements CASCADE;
-- DROP TABLE  curators CASCADE;
-- DROP TABLE  courses CASCADE;
-- DROP TABLE  users CASCADE;

-- Пользователи 
CREATE TABLE users
(
    user_id serial PRIMARY KEY,
    email text UNIQUE NOT NULL,
    username text UNIQUE NOT NULL,
    city text,
    avatar bytea NULL,
    password text -- NOT NULL
);
-- Курсы
CREATE TABLE courses
(
    course_id serial PRIMARY KEY,
    name text NOT NULL,
    avatar bytea,
    description text,
    category text,
    content json
);
-- Сайт
INSERT INTO courses(course_id, name) VALUES (0, 'Play'n'Study');
-- Кураторы
CREATE TABLE curators
(
    cur_rel_id serial PRIMARY KEY ,
    user_id integer REFERENCES users(user_id),
    course_id integer REFERENCES courses(course_id)
);
-- Ачивки
CREATE TABLE achievements
(
    ach_id serial PRIMARY KEY,
    course_id integer REFERENCES courses(course_id),
    name text UNIQUE NOT NULL,
    description text,
    condition text,
    image bytea
);
-- Задания
CREATE TABLE tasks
(
    task_id serial PRIMARY KEY,
    user_id integer REFERENCES users(user_id),
    name text NOT NULL,
    tags text[],
    description text,
    date date NOT NULL,
    completed boolean
);

CREATE TABLE achieve_rel
(
    ach_rel_id serial PRIMARY KEY ,
    ach_id integer REFERENCES achievements(ach_id),
    user_id integer REFERENCES users(user_id)
);

CREATE TABLE courses_rel
(
    cour_rel_id serial PRIMARY KEY,
    user_id integer REFERENCES users(user_id),
    course_id integer REFERENCES courses(course_id)
);

CREATE TABLE reviews(
    rev_id serial PRIMARY KEY,
    user_id int REFERENCES users(user_id),
    course_id int REFERENCES courses(course_id),
    rate int NOT NULL CHECK ( rate BETWEEN 0 AND 5),
    text text
);

CREATE TABLE sub_rel(
    sub_rel_id serial PRIMARY KEY,
    user_id int REFERENCES users(user_id),
    sub_id int REFERENCES users(user_id)
);

CREATE TABLE tests(
    test_id serial PRIMARY KEY,
    course_id int REFERENCES courses(course_id),
	unit_id int NOT NULL,
	avatar bytea NULL,
	description text, -- NEW!
    content json
);
-- Articles + File attach
CREATE TABLE articles(
    article_id serial PRIMARY KEY,
    course_id int REFERENCES courses(course_id),
	unit_id int NOT NULL,
	avatar bytea NULL,
	name text,
	description text,
    content text,
    score float
);

CREATE TABLE links( 
    link_id serial PRIMARY KEY,
    course_id int REFERENCES courses(course_id),
	unit_id int NOT NULL, 
	avatar bytea NULL,
	name text,
    link text
);

CREATE TABLE forums( 
    forum_id serial PRIMARY KEY,
    course_id int REFERENCES courses(course_id),
	unit_id int NOT NULL, 
	avatar bytea NULL,
	description text,
	score float,
	name text
);

CREATE TABLE forum_topics( 
    ft_id serial PRIMARY KEY,
    forum_id int REFERENCES forums(forum_id),
    is_active boolean DEFAULT TRUE,
	name text
);

CREATE TABLE topic_messages( 
    tm_id serial PRIMARY KEY,
    ft_id int REFERENCES forum_topics(ft_id),
    parent_tm_id int NULL,
	user_id int REFERENCES users(user_id),
	tm_date timestamp DEFAULT now(),
    content text
);

CREATE TABLE users_progress(
    up_id serial PRIMARY KEY ,
    user_id int REFERENCES users(user_id),
    course_id int REFERENCES courses(course_id),
	task_id int NOT NULL, -- (TASK = ARTICLE/TEST/LINK/FILE_ATTACH)
	task_type text,
	date_of_completion timestamp DEFAULT now(),
    progress json
);

CREATE TABLE roles(
    role_id serial PRIMARY KEY,
    name text
);

CREATE TABLE users_roles(
    ur_id serial PRIMARY KEY,
    user_id int REFERENCES users(user_id),
    role_id int REFERENCES roles(role_id)
);

-- ROLES
INSERT INTO roles(name) VALUES ('admin');


CREATE TABLE chats(
    chat_id serial PRIMARY KEY,
    user1 int REFERENCES users(user_id),
    user2 int REFERENCES users(user_id),
    last_change timestamp DEFAULT now(),
    user1_read boolean DEFAULT TRUE,
    user2_read boolean DEFAULT TRUE
);

CREATE TABLE chat_messages(
    msg_id serial PRIMARY KEY,
    chat_id int REFERENCES chats(chat_id),
    msg_text text,
    msg_date timestamp DEFAULT now(),
    msg_from int REFERENCES users(user_id),
    msg_to int REFERENCES users(user_id),
	user_to_read boolean DEFAULT FALSE
);

CREATE TABLE notifications(
    notif_id serial PRIMARY KEY,
    user_id integer REFERENCES users(user_id),
    notif_title text,
    notif_text text,
    notif_link text,
    receive_date timestamp DEFAULT now(),
	user_to_read boolean DEFAULT FALSE
);


CREATE TABLE notes(
    note_id serial PRIMARY KEY,
    user_id integer REFERENCES users(user_id),
    note_title text,
    note_text text,
    addition_date timestamp DEFAULT now()
);
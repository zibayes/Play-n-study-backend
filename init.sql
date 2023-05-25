-- DROP TABLE  articles CASCADE ;
-- DROP TABLE  users_progress CASCADE;
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


CREATE TABLE users
(
    user_id serial PRIMARY KEY,
    email text UNIQUE NOT NULL,
    username text UNIQUE NOT NULL,
    city text,
    avatar bytea NULL,
    password text NOT NULL
);

CREATE TABLE courses
(
    course_id serial PRIMARY KEY,
    name text NOT NULL,
    avatar text,
    description text,
    category text,
    content json
);

CREATE TABLE curators
(
    cur_rel_id serial PRIMARY KEY ,
    user_id integer REFERENCES users(user_id),
    course_id integer REFERENCES courses(course_id)
);

CREATE TABLE achievements
(
    ach_id serial PRIMARY KEY,
    course_id integer REFERENCES courses(course_id),
    name text UNIQUE NOT NULL,
    image bytea
);

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
    rate int NOT NULL CHECK ( rate BETWEEN 0 AND 10),
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
    content json
);

CREATE TABLE articles(
    article_id serial PRIMARY KEY,
    course_id int REFERENCES courses(course_id),
    content text
);

CREATE TABLE users_progress(
    up_id serial PRIMARY KEY ,
    user_id int REFERENCES users(user_id),
    course_id int REFERENCES courses(course_id),
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
    msg_to int REFERENCES users(user_id)
);


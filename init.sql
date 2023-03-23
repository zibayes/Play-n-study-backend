CREATE TABLE users
(
    user_id serial PRIMARY KEY,
    email text UNIQUE NOT NULL,
    username varchar(20) UNIQUE NOT NULL,
    city text,
    avatar text,
    password text NOT NULL
);

CREATE TABLE courses
(
    course_id serial PRIMARY KEY,
    name text NOT NULL,
    avatar text
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
    image text
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

import json
# todo: поправить json'ы или убрать там где не нужно

class User:
    def __init__(self, user_id=0, email=None, username=None, city=None, avatar=None, password=None):
        self.user_id = user_id
        self.email = email
        self.username = username
        self.city = city
        self.avatar = avatar
        self.password = password

        # query fields
        self.achievements = None
        self.courses = None
        self.courses_count = 0
        self.subs = None
        self.subs_count = 0
        self.sub_to = None
        self.sub_to_count = 0


class Achievement:
    def __init__(self, ach_id=0, course_id=0, name=None, image=None):
        self.ach_id = ach_id
        self.course_id = course_id
        self.name = name
        self.image = image


class AchieveRel:
    def __init__(self, ach_rel_id=0, ach_id=0, user_id=0):
        self.ach_rel_id = ach_rel_id
        self.ach_id = ach_id
        self.user_id = user_id


class Course:
    def __init__(self, course_id=0, name=None, avatar=None, description=None, category=None, content=None):
        self.course_id = course_id
        self.name = name
        self.avatar = avatar
        self.description = description
        self.category = category
        self.content = content

class CourseRel:
    def __init__(self, cour_rel_id=0, user_id=0, course_id=0):
        self.cour_rel_id = cour_rel_id
        self.user_id = user_id
        self.course_id = course_id

    def json(self):
        return json.dumps({
            "cour_rel_id": self.cour_rel_id,
            "user_id": self.user_id,
            "course_id": self.course_id
        })

class Curator:
    def __init__(self, cur_id=0, user_id=0, course_id=0):
        self.cur_id = cur_id
        self.user_id = user_id
        self.course_id = course_id

    def json(self):
        return {
            "cur_id": self.cur_id,
            "user_id": self.user_id,
            "course_id": self.course_id
        }

class Review:
    def __init__(self, rev_id=0, user_id=0, course_id=0, rate=0, text=None):
        self.rev_id = rev_id
        self.user_id = user_id
        self.course_id = course_id
        self.rate = rate
        self.text = text

    def json(self):
        return {
            "rev_id": self.rev_id,
            "user_id": self.user_id,
            "course_id": self.course_id,
            "rate": self.rate,
            "text": self.text
        }

class SubRel:
    def __init__(self, sub_rel_id=0, user_id=0, sub_id=0):
        self.sub_rel_id = sub_rel_id
        self.user_id = user_id
        self.sub_id = sub_id

    def json(self):
        return {
            "sub_rel_id": self.sub_rel_id,
            "user_id": self.user_id,
            "sub_id": self.sub_id
        }

class Task:
    def __init__(self, task_id=0, user_id=0, name=None, tags=None, description=None, _date=None, completed=False):
        self.task_id = task_id
        self.user_id = user_id
        self.name = name
        self.tags = tags
        self.description = description
        self.date = _date
        self.completed = completed

    def json(self):
        return {
            "task_id": self.task_id,
            "user_id": self.user_id,
            "name": self.name,
            "tags": self.tags,
            "description": self.description,
            "date": self.date,
            "completed": self.completed
        }



def downcast(base, derived):
    derived.ask = base.ask
    derived.answers = base.answers
    derived.correct = base.correct
    derived.score = base.score
    derived.type = base.type
    return derived


def upcast(derived, base):
    base.ask = derived.ask
    base.answers = derived.answers
    base.correct = derived.correct
    base.score = derived.score
    base.type = derived.type
    return base


class Test:
    def __init__(self, test_id, course_id, content):
        self.test_id = test_id
        self.course_id = course_id
        self.content = content


class TestContent:
    def __init__(self, name=None, questions=None):
        self.name = name
        self.questions = questions

    @staticmethod
    def from_json(test_json):
        test_json = json.loads(test_json)
        new_test = TestContent(name=test_json['name'])
        test_questions = []
        questions = test_json['questions']
        for question in questions:
            match question['type']:
                case 'solo':
                    test_questions.append(QSolo.from_json(question))
                case 'multiple':
                    test_questions.append(QMultiple.from_json(question))
                case 'free':
                    test_questions.append(QFree.from_json(question))
                case 'detailed_free':
                    test_questions.append(QDetailedFree.from_json(question))
                case 'info':
                    test_questions.append(QInfo.from_json(question))

        new_test.questions = test_questions
        return new_test

    def toJSON(self):
        json_test = {"name": self.name}
        questions = []
        for question in self.questions:
            questions.append(Question.toJSON(upcast(question, Question())))
        json_test['questions'] = questions
        return json.dumps(json_test, ensure_ascii=False)


class Question:
    def __init__(self, ask=None, answers=None, correct=None, score=None, type=None):
        self.ask = ask if ask != 'null' else None
        self.answers = None if answers == 'null' else answers
        self.correct = None if correct == 'null' else correct
        self.score = None if score == 'null' else score
        self.type = None if type == 'null' else type

    @staticmethod
    def from_json(qbase_json):
        return Question(qbase_json['ask'], qbase_json['answers'], qbase_json['correct'],
                        qbase_json['score'], qbase_json['type'])

    def toJSON(self):
        return {
            "ask": self.ask,
            "answers": self.answers,
            "correct": self.correct,
            "score": self.score,
            "type": self.type
        }

    @staticmethod
    def downcast(base, derived):
        derived.ask = base.ask
        derived.answers = base.answers
        derived.correct = base.correct
        derived.score = base.score
        derived.type = base.type
        return derived


class QInfo(Question):
    def __init__(self, ask, type):
        super().__init__(ask=ask, type=ask)

    @staticmethod
    def from_json(qinfo_json):
        base = Question.from_json(qinfo_json)
        return downcast(base, QInfo(None, None))


class QDetailedFree(Question):
    def __init__(self, ask, type, score):
        super().__init__(ask=ask, type=type, score=score)

    @staticmethod
    def from_json(qdetailed_json):
        base = Question.from_json(qdetailed_json)
        return downcast(base, QDetailedFree(None, None, None))


class QFree(Question):
    def __init__(self, ask, answers, correct, score, type):
        super().__init__(ask, answers, correct, score, type)

    @staticmethod
    def from_json(qfree_json):
        base = Question.from_json(qfree_json)
        return downcast(base, QFree(None, None, None, None, None))


class QMultiple(Question):
    def __init__(self, ask, answers, correct, score, type):
        super().__init__(ask, answers, correct, score, type)

    @staticmethod
    def from_json(qmultiple_json):
        base = Question.from_json(qmultiple_json)
        return downcast(base, QMultiple(None, None, None, None, None))


class QSolo(Question):
    def __init__(self, ask, answers, correct, score, type):
        super().__init__(ask, answers, correct, score, type)

    @staticmethod
    def from_json(qsolo_json):
        base = Question.from_json(qsolo_json)
        return downcast(base, QSolo(None, None, None, None, None))


# контент курсов

class CourseUnit:
    def __init__(self, unit_type=None, unit_id=None):
        self.unit_type = unit_type
        self.unit_id = unit_id

    @staticmethod
    def from_json(unit_json):
        return {
            CourseUnit(unit_type=unit_json['unit_type'], unit_id=unit_json['unit_id'])
        }

    def to_json(self):
        return json.dumps({
            "unit_type": self.unit_type,
            "unit_id": self.unit_id
        })


class Article:
    def __init__(self, article_id, course_id, content):
        self.article_id = article_id
        self.course_id = course_id
        self.content = content

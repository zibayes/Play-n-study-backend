import json
from flask_login import current_user


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
        self.notifications = None
        self.notifications_count = 0


class Achievement:
    def __init__(self, ach_id=0, course_id=0, description=None, condition=None, name=None, image=None):
        self.ach_id = ach_id
        self.course_id = course_id
        self.name = name
        self.description = description
        self.condition = condition
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
    derived.shuffle = base.shuffle
    derived.correct = base.correct
    derived.score = base.score
    derived.current_score = base.current_score
    derived.type = base.type
    derived.comment = base.comment
    derived.file = base.file
    return derived


def upcast(derived, base):
    base.ask = derived.ask
    base.answers = derived.answers
    base.shuffle = derived.shuffle
    base.correct = derived.correct
    base.score = derived.score
    base.current_score = derived.current_score
    base.type = derived.type
    base.comment = derived.comment
    base.file = derived.file
    return base


class Test:
    def __init__(self, test_id, course_id, unit_id, content, avatar=None, description=None):
        self.test_id = test_id
        self.course_id = course_id
        self.unit_id = unit_id
        self.content = content
        self.avatar = avatar
        self.description = description


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
                case 'compliance':
                    test_questions.append(QCompliance.from_json(question))
                case 'filling_gaps':
                    test_questions.append(QFillingGaps.from_json(question))
                case 'drag_to_text':
                    test_questions.append(QDragToText.from_json(question))
                case 'markers_drag':
                    test_questions.append(QMarkersDrag.from_json(question))
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
    def __init__(self, ask=None, answers=None, shuffle=None, correct=None, score=None,
                 current_score=None, type=None, comment=None, file=None):
        self.ask = ask if ask != 'null' else None
        self.answers = None if answers == 'null' else answers
        self.shuffle = None if shuffle == 'null' else shuffle
        self.correct = None if correct == 'null' else correct
        self.score = None if score == 'null' else score
        self.current_score = None if current_score == 'null' else current_score
        self.type = None if type == 'null' else type
        self.comment = None if comment == 'null' else comment
        self.file = None if file == 'null' else file

    @staticmethod
    def from_json(qbase_json):
        return Question(qbase_json['ask'], qbase_json['answers'], qbase_json['shuffle'], qbase_json['correct'],
                        qbase_json['score'], qbase_json['current_score'], qbase_json['type'], qbase_json['comment'],
                        qbase_json['file'])

    def toJSON(self):
        return {
            "ask": self.ask,
            "answers": self.answers,
            "shuffle": self.shuffle,
            "correct": self.correct,
            "score": self.score,
            "current_score": self.current_score,
            "type": self.type,
            "comment": self.comment,
            "file": self.file
        }

    @staticmethod
    def downcast(base, derived):
        derived.ask = base.ask
        derived.answers = base.answers
        derived.shuffle = base.shuffle
        derived.correct = base.correct
        derived.score = base.score
        derived.current_score = base.current_score
        derived.type = base.type
        derived.comment = base.comment
        derived.file = base.file
        return derived


class QInfo(Question):
    def __init__(self, ask, type):
        super().__init__(ask=ask, type=type)

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


class QMarkersDrag(Question):
    def __init__(self, ask, answers, shuffle, correct, score, type):
        super().__init__(ask, answers, shuffle, correct, score, type)

    @staticmethod
    def from_json(qmarkers_drag_json):
        base = Question.from_json(qmarkers_drag_json)
        return downcast(base, QMarkersDrag(None, None, None, None, None, None))


class QDragToText(Question):
    def __init__(self, ask, answers, shuffle, correct, score, type):
        super().__init__(ask, answers, shuffle, correct, score, type)

    @staticmethod
    def from_json(qdrag_to_text_json):
        base = Question.from_json(qdrag_to_text_json)
        return downcast(base, QDragToText(None, None, None, None, None, None))


class QFillingGaps(Question):
    def __init__(self, ask, answers, shuffle, correct, score, type):
        super().__init__(ask, answers, shuffle, correct, score, type)

    @staticmethod
    def from_json(qfilling_gaps_json):
        base = Question.from_json(qfilling_gaps_json)
        return downcast(base, QFillingGaps(None, None, None, None, None, None))


class QCompliance(Question):
    def __init__(self, ask, answers, shuffle, correct, score, type):
        super().__init__(ask, answers, shuffle, correct, score, type)

    @staticmethod
    def from_json(qcompliance_json):
        base = Question.from_json(qcompliance_json)
        return downcast(base, QCompliance(None, None, None, None, None, None))


class QMultiple(Question):
    def __init__(self, ask, answers, shuffle, correct, score, type):
        super().__init__(ask, answers, shuffle, correct, score, type)

    @staticmethod
    def from_json(qmultiple_json):
        base = Question.from_json(qmultiple_json)
        return downcast(base, QMultiple(None, None, None, None, None, None))


class QSolo(Question):
    def __init__(self, ask, answers, shuffle, correct, score, type):
        super().__init__(ask, answers, shuffle, correct, score, type)

    @staticmethod
    def from_json(qsolo_json):
        base = Question.from_json(qsolo_json)
        return downcast(base, QSolo(None, None, None, None, None, None))


# контент курсов

class CourseUnit:
    def __init__(self, unit_type=None, unit_id=None, test_id=None, test=None):
        self.unit_type = unit_type
        self.unit_id = unit_id
        self.test_id = test_id
        self.test = test

    @staticmethod
    def from_json(unit_json):
        return {
            'body': [
                {
                 'name': unit['name'],
                 'unit_id': unit['unit_id'],
                 'tests': [
                    CourseUnit(unit_type=i['unit_type'], test_id=i['test_id']) for i in unit['tests']
                 ]
                } for unit in unit_json['body']
            ],
            'unit_counter': unit_json['unit_counter']
        }

    @staticmethod
    def to_json(units):
        return json.dumps({
            'body': [
                {
                 'name': unit['name'],
                 'unit_id': unit['unit_id'],
                 'tests': [
                     {
                      'unit_type': i['unit_type'] if isinstance(i, dict) else i.unit_type,
                      'test_id': i['test_id'] if isinstance(i, dict) else i.test_id
                     } for i in unit['tests']
                 ]
                } for unit in units['body']
            ],
            'unit_counter': units['unit_counter']
        })


class Article:
    def __init__(self, article_id, course_id, unit_id, content, name, score, description=None, avatar=None):
        self.article_id = article_id
        self.course_id = course_id
        self.unit_id = unit_id
        self.avatar = avatar
        self.name = name
        self.description = description
        self.content = content
        self.score = score


class UserProgress:
    def __init__(self, up_id, user_id, course_id, task_id, task_type, progress):
        self.up_id = up_id
        self.user_id = user_id
        self.course_id = course_id
        self.task_id = task_id
        self.task_type = task_type
        # это поле типа Progress
        self.progress = progress


class Progress:
    def __init__(self, progress_id, test_id, type, completed, result=None, content=None):
        self.progress_id = progress_id
        self.test_id = test_id
        self.type = type
        self.completed = completed
        # это поле типа TestResult
        self.result = result
        # это поле типа TestContent
        self.content = content

    @staticmethod
    def to_json(progress):
        return json.dumps({
            'content': progress.content,
            'result': progress.result,
            'progress_id': progress.progress_id,
            'test_id': progress.test_id,
            'completed': progress.completed,
            'type': progress.type
        })

    @staticmethod
    def from_json(progress_json):
        # return Progress(progress_json['content'], progress_json['result'], progress_json['progress_id'], progress_json['test_id'], progress_json['completed'], progress_json['type'])
        return {
            'content': progress_json['content'],
            'result': progress_json['result'],
            'progress_id': progress_json['progress_id'],
            'test_id': progress_json['test_id'],
            'completed': progress_json['completed'],
            'type': progress_json['type']
        }


class ChatMessage:
    def __init__(self, msg_id, chat_id, msg_text, msg_date, msg_from, msg_to, user_to_read):
        self.msg_id = msg_id
        self.chat_id = chat_id
        self.msg_text = msg_text
        self.msg_date = msg_date
        self.msg_from = msg_from
        self.msg_to = msg_to
        self.user_to_read = user_to_read

    def to_dict(self):
        return {
            "msg_id": self.msg_id,
            "chat_id": self.chat_id,
            "msg_text": self.msg_text,
            "msg_date": self.msg_date,
            "msg_from": self.msg_from,
            "msg_to": self.msg_to,
            "user_to_read": self.user_to_read
        }


class Chat:
    def __init__(self, chat_id, user_with, last_change, checked):
        self.chat_id = chat_id
        self.user_with = user_with
        self.last_change = last_change
        self.checked = checked


class ChatPreview:
    def __init__(self, user_with, last_message, from_who, time, user_with_id, checked, chat_id, msg_new_count, from_who_id):
        self.user_with = user_with
        self.last_message = last_message
        self.from_who = from_who
        self.time = time
        self.user_with_id = user_with_id
        self.checked = checked
        self.chat_id = chat_id
        self.msg_new_count = msg_new_count
        self.from_who_id = from_who_id

    def to_dict(self):
        return {
            "user_with": self.user_with,
            "last_message": self.last_message,
            "from_who": self.from_who,
            "time": self.time,
            "user_with_id": self.user_with_id,
            "checked": self.checked,
            "chat_id": self.chat_id,
            "msg_new_count": self.msg_new_count,
            "from_who_id": self.from_who_id
        }


class Link:
    def __init__(self, link_id, course_id, unit_id, name, link, avatar=None):
        self.link_id = link_id
        self.course_id = course_id
        self.unit_id = unit_id
        self.avatar = avatar
        self.name = name
        self.link = link


class FileAttach:
    def __init__(self, attach_id, course_id, unit_id, name, description=None, avatar=None, content=None):
        self.attach_id = attach_id
        self.course_id = course_id
        self.unit_id = unit_id
        self.avatar = avatar
        self.name = name
        self.description = description
        self.content = content


class Forum:
    def __init__(self, forum_id, course_id, unit_id, name, score, description=None, avatar=None):
        self.forum_id = forum_id
        self.course_id = course_id
        self.unit_id = unit_id
        self.avatar = avatar
        self.score = score
        self.name = name
        self.description = description


class ForumTopic:
    def __init__(self, ft_id, forum_id, name, is_active):
        self.ft_id = ft_id
        self.forum_id = forum_id
        self.name = name
        self.is_active = is_active


class TopicMessage:
    def __init__(self, tm_id, ft_id, parent_tm_id, user_id, tm_date, content):
        self.tm_id = tm_id
        self.ft_id = ft_id
        self.parent_tm_id = parent_tm_id
        self.user_id = user_id
        self.tm_date = tm_date
        self.content = content


class Notification:
    def __init__(self, notif_id, user_id, notif_title, notif_text, notif_link, receive_date, user_to_read):
        self.notif_id = notif_id
        self.user_id = user_id
        self.notif_title = notif_title
        self.notif_text = notif_text
        self.notif_link = notif_link
        self.receive_date = receive_date
        self.user_to_read = user_to_read


class Note:
    def __init__(self, note_id, user_id, note_title, note_text, addition_date):
        self.note_id = note_id
        self.user_id = user_id
        self.note_title = note_title
        self.note_text = note_text
        self.addition_date = addition_date


class Deadline:
    def __init__(self, deadline_id, course_id, task_type, task_id, user_id, title, start_date, end_date):
        self.deadline_id = deadline_id
        self.course_id = course_id
        self.task_type = task_type
        self.task_id = task_id
        self.user_id = user_id
        self.title = title
        self.start_date = start_date
        self.end_date = end_date


class Level:
    def __init__(self, level_id, course_id, names, scores):
        self.level_id = level_id
        self.course_id = course_id
        self.names = names
        self.scores = scores
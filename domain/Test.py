import json


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

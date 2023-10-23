import copy
import time
import json

from data.types import TestContent, Question, Test


class TestResult:
    def __init__(self, total_score, total_current_score, total_time, result):
        self.total_score = total_score
        self.total_current_score = total_current_score
        self.total_time = total_time
        self.result = result

    def to_json(self):
        return json.dumps({
            'total_score': self.total_score,
            'total_current_score': self.total_current_score,
            'total_time': self.total_time,
            'result': self.result
        })

    @staticmethod
    def from_json(result_json):
        return TestResult(result_json['total_score'], result_json['total_current_score'],
                          result_json['total_time'], result_json['result'])


def get_test_from_form(form, unit_id=None, test_id=None, course_id=1):
    test_form = form.to_dict()
    test_name = test_form.pop("testName")
    test_desc = test_form.pop("testDesc")
    questions_count = 0
    for key in test_form.keys():
        if "Question-" in key:
            questions_count += 1
    test_body = []
    score = 0
    for i in range(questions_count):
        right_answers_count = 0
        question = Question()
        for key, value in test_form.items():
            if "Question-" in key:
                question.ask = value
                question.answers = []
            if "QuestionType-" in key: # TODO: поменять с содержимого текста на id или name!
                if value == "Единственный ответ":
                    question.type = "solo"
                if value == "Множественный ответ":
                    question.type = "multiple"
                if value == "На соответствие":
                    question.type = "compliance"
                if value == "Заполнение пропусков":
                    question.type = "filling_gaps"
                if value == "Перетаскивание в текст":
                    question.type = "drag_to_text"
                if value == "Перетаскивание маркеров":
                    question.type = "markers_drag"
                if value == "Краткий свободный ответ":
                    question.type = "free"
                if value == "Свободный ответ":
                    question.type = "detailed_free"
                if value == "Информационный блок":
                    question.type = "info"
                break
        new_form = copy.deepcopy(test_form)
        if question.type == "compliance":
            for key, value in test_form.items():
                if "QuestionCom-" in key:
                    right_answers_count += 1
                    question.answers.append({value: ""})
                if "Answer-" in key and "Right_Answer-" not in key:
                    question.answers[-1][list(question.answers[-1].keys())[0]] = value
                if "score-" in key:
                    question.score = int(value)
                    score += int(value)
                if "Shuffle-" in key:
                    question.shuffle = value
                if "QuestionType-" in key:
                    question.correct = right_answers_count
                    new_form.pop(key)
                    break
                new_form.pop(key)
            test_form = new_form
        if question.type in ("filling_gaps", "drag_to_text"):
            for key, value in test_form.items():
                if "Answer-" in key and "Right_Answer-" not in key:
                    right_answers_count += 1
                    question.answers.append({"answer": value, "mark": key[key.rfind('-')+1:]})
                if "Group-" in key:
                    question.answers[-1]['group'] = value
                if "score-" in key:
                    question.score = int(value)
                    score += int(value)
                if "Shuffle-" in key:
                    question.shuffle = value
                if "QuestionType-" in key:
                    question.correct = right_answers_count
                    new_form.pop(key)
                    break
                new_form.pop(key)
            test_form = new_form
        if question.type == "markers_drag":
            for key, value in test_form.items():
                if "Marker-" in key:
                    right_answers_count += 1
                    question.answers.append({"marker": value})
                if "ZoneFigure-" in key:
                    question.answers[-1]['figure'] = value
                if "Coordinates-" in key:
                    question.answers[-1]['coordinates'] = value
                if "File-" in key:
                    question.file = value
                if "score-" in key:
                    question.score = int(value)
                    score += int(value)
                if "Shuffle-" in key:
                    question.shuffle = value
                if "QuestionType-" in key:
                    question.correct = right_answers_count
                    new_form.pop(key)
                    break
                new_form.pop(key)
            test_form = new_form
        if question.type in ("solo", "multiple",):
            is_right_answer = False
            for key, value in test_form.items():
                if "Answer-" in key and "Right_Answer-" not in key:
                    question.answers.append({value: is_right_answer})
                    is_right_answer = False
                if "Right_Answer-" in key:
                    right_answers_count += 1
                    is_right_answer = True
                if "score-" in key:
                    question.score = int(value)
                    score += int(value)
                if "Shuffle-" in key:
                    question.shuffle = value
                if "QuestionType-" in key:
                    question.correct = right_answers_count
                    new_form.pop(key)
                    break
                new_form.pop(key)
            test_form = new_form
        if question.type == "free":
            for key, value in test_form.items():
                if "Answer-" in key and "Right_Answer-" not in key:
                    question.answers.append(value)
                if "score-" in key:
                    question.score = int(value)
                    score += int(value)
                if "QuestionType-" in key:
                    new_form.pop(key)
                    break
                new_form.pop(key)
            test_form = new_form
        if question.type in ("detailed_free", "info"):
            for key, value in test_form.items():
                if "score-" in key:
                    if question.type == "detailed_free":
                        question.score = int(value)
                        score += int(value)
                if "QuestionType-" in key:
                    new_form.pop(key)
                    break
                new_form.pop(key)
            test_form = new_form
        test_body.append(question)
    test_content = TestContent(test_name, test_body)

    return Test(test_id, course_id, unit_id, test_content.toJSON(), description=test_desc)


def get_test_result(test, form):
    total_current_score = 0
    total_score = 0
    test_res = form.to_dict()
    total_time = time.time() - float(test_res['time'])
    for question in test.content.questions:
        question.current_score = 0
        answers_count = 0
        score_part = 0
        for key, value in test_res.items():
            if key == question.ask or question.ask + '-' in key:
                if question.type in ("solo", "multiple"):
                    for que_part in question.answers:
                        if value in que_part.keys():
                            if que_part[value]:
                                que_part[value] = "right"
                                score_part += question.score / question.correct
                            else:
                                que_part[value] = "wrong"
                                if question.type == "multiple":
                                    score_part -= question.score / question.correct  # (question.correct * 2)
                            answers_count += 1
                elif question.type in ("compliance", "filling_gaps"):
                    for que_part in question.answers:
                        if value in que_part.keys():
                            if que_part[value]:
                                que_part[value] = "right"
                                score_part += question.score / question.correct
                            else:
                                que_part[value] = "wrong"
                                score_part -= question.score / question.correct  # (question.correct * 2)
                            answers_count += 1
                elif question.type == "free":
                    question.answers.append(value)
                    question.is_correct = False
                    for answer in question.answers[:1]:
                        if value.lower().strip() == answer.lower().strip():
                            question.current_score += question.score
                            question.is_correct = True
                elif question.type == "detailed_free":
                    question.answers.append(value)
                    question.current_score = None
        if (score_part < 0 or (answers_count == len(question.answers) and question.correct != len(question.answers))) \
                and question.type == "multiple":
            score_part = 0
        if question.current_score is not None:
            question.current_score += score_part
        if question.score:
            total_score += question.score
            if question.current_score is not None:
                total_current_score += question.current_score
        # if question.current_score < 0 or answers_count == len(question.answers):
        #     question.current_score = 0
        if question.current_score is not None:
            question.current_score = ("%.2f" % question.current_score).replace(".00", "")
    result = round(float(total_current_score) / float(total_score) * 100, 2)
    return TestResult(total_score, total_current_score, total_time, result)

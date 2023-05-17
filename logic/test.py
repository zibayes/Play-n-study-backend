import copy
import time

from data.types import TestContent, Question, Test


class TestResult:
    def __init__(self, total_score, total_current_score, total_time, result):
        self.total_score = total_score
        self.total_current_score = total_current_score
        self.total_time = total_time
        self.result = result


def get_test_from_form(form, test_id=None, course_id=1):
    test_form = form.to_dict()
    print(test_form)
    test_name = test_form.pop("testName")
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
            if "QuestionType-" in key:
                if value == "Единственный ответ":
                    question.type = "solo"
                if value == "Множественный ответ":
                    question.type = "multiple"
                if value == "Краткий свободный ответ":
                    question.type = "free"
                if value == "Свободный ответ":
                    question.type = "detailed_free"
                if value == "Информационный блок":
                    question.type = "info"
                break
        new_form = copy.deepcopy(test_form)
        if question.type in ("solo", "multiple"):
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

    return Test(test_id, course_id, test_content.toJSON())


def get_test_result(test, form):
    total_current_score = 0
    total_score = 0
    test_res = form.to_dict()
    total_time = time.time() - float(test_res['time'])
    for question in test.content.questions:
        question.current_score = 0
        answers_count = 0
        for key, value in test_res.items():
            if key == question.ask or question.ask + '-' in key:
                if question.type in ("solo", "multiple"):
                    for que_part in question.answers:
                        if value in que_part.keys():
                            if que_part[value]:
                                que_part[value] = "right"
                                question.current_score += question.score / question.correct
                            else:
                                que_part[value] = "wrong"
                                question.current_score -= question.score / question.correct  # (question.correct * 2)
                            answers_count += 1
                elif question.type in ("free", "detailed_free"):
                    question.answer = value
                    question.is_correct = False
                    for answer in question.answers:
                        if value.lower().strip() == answer.lower().strip():
                            question.current_score += question.score
                            question.is_correct = True
        if question.score:
            total_score += question.score
            total_current_score += question.current_score
        if question.current_score < 0 or answers_count == len(question.answers):
            question.current_score = 0
        question.current_score = ("%.2f" % question.current_score).replace(".00", "")
    result = round(float(total_current_score) / float(total_score) * 100, 2)
    return TestResult(total_score, total_current_score, total_time, result)

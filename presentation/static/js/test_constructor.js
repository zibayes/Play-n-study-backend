import { addDragoverEventListener, addQuestionListener } from './test_constructor_functions.js';

let questions_list = document.getElementById("questionsList")
addDragoverEventListener(questions_list, `question_div`);
// Добавление вопроса
let addBtn = document.getElementById("addQuestion");
window.questionIndex = 1;
window.answerIndex = 0;
addQuestionListener(addBtn);
window.canvases  = new Map();
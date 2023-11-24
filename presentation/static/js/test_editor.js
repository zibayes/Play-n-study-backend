import {
    addDragoverEventListener,
    addQuestionListener,
    addDragndropDesignVoid,
    questionTypeSet
} from './test_constructor_functions.js';

let questions_list = document.getElementById("questionsList")
let dnd_elems = []
let card_elems = []
let questionsTypes = []
let addAns_elems = []
let i
for(i = 1; i <= questions_count; i++){
    dnd_elems.push(document.getElementById("dnd-" + i))
    card_elems.push(document.getElementById("card-" + i))
    addDragndropDesignVoid(card_elems, dnd_elems[i-1], 'editor')

    questionsTypes.push(document.getElementById("QT-" + i))
    let textareaQuestion = document.getElementById("ask-" + (parseInt(questionsTypes[i-1].name.slice(13))))
    questionTypeSet(questionsTypes[i-1], textareaQuestion, parseInt(questionsTypes[i-1].name.slice(13)))

    addAns_elems.push(document.getElementById("addAns-" + i))
    addDragoverEventListener(addAns_elems, `editor`, i, questions_list)
}

document.querySelectorAll(".dnd").forEach(elem =>{
    let divTextLabel = document.getElementById("Answer-" + elem.id);
    addDragndropDesignVoid(divTextLabel, elem, 'answer');
});

addDragoverEventListener(questions_list, `question_div`)

// Добавление вопроса
let addBtn = document.getElementById("addQuestion");
window.questionIndex = questions_count + 1;
//window.answerIndex = 0;
addQuestionListener(addBtn);
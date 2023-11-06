import {
    arrLang
} from './translate_dictionary.js';

import {
    draw_figures,
    myDown,
    myUp,
    myMove
} from './markers_drag_functions.js';

window.draw_figures = draw_figures;

// Функция добавления слушателя события перетаскивания
export function addDragoverEventListener(dragndropArea, tagContains, i=undefined, questions_list=undefined) {
    let isAbleToMove = true;
    let areaArray;
    if(tagContains === 'editor'){
        areaArray = dragndropArea;
        dragndropArea = dragndropArea[i-1];
    }
    dragndropArea.addEventListener(`dragover`, (evt) => {
        // Разрешаем сбрасывать элементы в эту область
        evt.preventDefault();

        // Находим перемещаемый элемент
        let activeElement;
        let currentElement;
        if(tagContains !== 'editor') {
            activeElement = dragndropArea.querySelector(`.selected`);
            // Находим элемент, над которым в данный момент находится курсор
            currentElement = evt.target;
        } else {
            activeElement = questions_list.querySelector(`.selected`);
            // Находим элемент, над которым в данный момент находится курсор
            currentElement = evt.target.parentElement.parentElement;
        }
        // Проверяем, что событие сработало:
        // 1. не на том элементе, который мы перемещаем,
        // 2. именно на элементе списка
        let isMoveable;
        if(tagContains === "question_div" || tagContains === "unit_div"){
            isMoveable = activeElement !== currentElement && isAbleToMove &&
        currentElement.classList.contains(tagContains) && activeElement.classList.contains(tagContains);
        } else if(tagContains === "answer_div"){
            isMoveable = activeElement !== currentElement && isAbleToMove &&
        currentElement.classList.contains(tagContains) && activeElement.classList.contains(tagContains) && childOf(activeElement, dragndropArea);
        } else if(tagContains === 'editor') {
            isMoveable = activeElement !== currentElement && isAbleToMove &&
        currentElement.classList.contains(`answer_div`) && activeElement.classList.contains(`answer_div`) && childOf(activeElement, areaArray[parseInt(evt.target.id)-1]);
        }
        // Если нет, прерываем выполнение функции
        if (!isMoveable)
            return;
        isAbleToMove = false;

        // Находим элемент, перед которым будем вставлять
        let nextElement;
        if(currentElement === activeElement.nextElementSibling){
            nextElement = currentElement.nextElementSibling;
            currentElement.animate(
              [
                // Ключевые кадры
                { transform: "translateY(" + activeElement.offsetHeight + "px)" },
                { transform: "translateY(" + 0 + "px)" },
              ],
              {
                // Настройки времени
                duration: 300,
                iterations: 1,
              }
            );
        } else {
            nextElement = currentElement;
            currentElement.animate(
              [
                // Ключевые кадры
                { transform: "translateY(-" + activeElement.offsetHeight + "px)" },
                { transform: "translateY(" + 0 + "px)" },
              ],
              {
                // Настройки времени
                duration: 300,
                iterations: 1,
              }
            );
        }

        // Вставляем activeElement перед nextElement
        if(tagContains !== 'editor') {
            dragndropArea.insertBefore(activeElement, nextElement);
        } else{
            areaArray[parseInt(evt.target.id)-1].insertBefore(activeElement, nextElement);
        }
        setTimeout(() => {isAbleToMove = true;}, 400)
    });
}

// Функция проверки элемента на то, что он является дочерним относительно другого элемента
export function childOf(c,p){while((c=c.parentNode)&&c!==p);return !!c}

// Добавление ответа на вопрос
window.addAnswerOnButtonClick = function(index){
    let questionType = document.getElementById(`QT-${index.substring(7)}`);
    let selectedOption = questionType.options[questionType.selectedIndex];

    let div = document.createElement('div');
    div.setAttribute('style', "padding-bottom: 10px; display: flex; align-items: center;");
    div.setAttribute('id', "delAns-" + answerIndex);
    div.setAttribute('class', "answer_div");

    let divMarker, textareaMarker, divZone, circleVis, polygon, divCoords//, textareaCoords, window.zoneType;
    if(selectedOption.getAttribute('key') === "markers_drag") {
        window.zones.set(questionIndex + "-" + answerIndex, {vertexes:[{x:10,y:10,v:false},{x:10,y:60,v:false},{x:60,y:60,v:false},{x:60,y:10,v:false}],isDragging:false,selected:false,marker_name:""});

        divMarker = document.createElement('div');
        divMarker.setAttribute('style', "width: 75px; margin-right: 4px;");
        divMarker.setAttribute('key', "marker");
        divMarker.setAttribute('class', "lang");
        divMarker.textContent = "Маркер";
        textareaMarker = document.createElement('textarea');
        textareaMarker.setAttribute('class', "form-control langp");
        textareaMarker.setAttribute('key', "marker_name");
        textareaMarker.setAttribute('placeholder', "Название маркера");
        textareaMarker.setAttribute('name', "Marker-" + questionIndex + "-" + answerIndex);
        textareaMarker.setAttribute('id', "Marker-" + questionIndex + "-" + answerIndex);
        textareaMarker.setAttribute('rows', "1");
        textareaMarker.setAttribute('maxlength', '5000');
        textareaMarker.setAttribute('value', '');
        divZone = document.createElement('div');
        divZone.setAttribute('style', "width: 450px; margin-left: 8px; margin-right: 2px;");
        divZone.setAttribute('key', "zone_type");
        divZone.setAttribute('class', "lang");
        divZone.textContent = "Форма зоны";
        window.zones.get(textareaMarker.id.substring(7)).zoneType = document.createElement('select')
        window.zones.get(textareaMarker.id.substring(7)).zoneType.setAttribute('class', "form-select");
        window.zones.get(textareaMarker.id.substring(7)).zoneType.setAttribute('style', "width: 180px;");
        window.zones.get(textareaMarker.id.substring(7)).zoneType.setAttribute('id', "ZoneFigure-" + questionIndex + "-" + answerIndex);
        window.zones.get(textareaMarker.id.substring(7)).zoneType.setAttribute('name', "ZoneFigure-" + questionIndex + "-" + answerIndex);
        circleVis = document.createElement('option')
        circleVis.setAttribute('class', "lang");
        circleVis.setAttribute('key', "circle");
        circleVis.textContent = "Окружность"
        polygon = document.createElement('option')
        polygon.setAttribute('class', "lang");
        polygon.setAttribute('key', "polygon");
        polygon.textContent = "Многоугольник"
        divCoords = document.createElement('div');
        divCoords.setAttribute('style', "width: 160px; margin-left: 8px; margin-right: 4px;");
        divCoords.setAttribute('key', "coordinates");
        divCoords.setAttribute('class', "lang");
        divCoords.textContent = "Координаты";
        window.zones.get(textareaMarker.id.substring(7)).textareaCoords = document.createElement('textarea');
        window.zones.get(textareaMarker.id.substring(7)).textareaCoords.setAttribute('class', "form-control langp");
        window.zones.get(textareaMarker.id.substring(7)).textareaCoords.setAttribute('key', "zone_coordinates");
        window.zones.get(textareaMarker.id.substring(7)).textareaCoords.setAttribute('placeholder', "Координаты зоны");
        window.zones.get(textareaMarker.id.substring(7)).textareaCoords.setAttribute('name', "Coordinates-" + questionIndex + "-" + answerIndex);
        window.zones.get(textareaMarker.id.substring(7)).textareaCoords.setAttribute('id', "Coordinates-" + questionIndex + "-" + answerIndex);
        window.zones.get(textareaMarker.id.substring(7)).textareaCoords.setAttribute('rows', "1");
        window.zones.get(textareaMarker.id.substring(7)).textareaCoords.setAttribute('maxlength', '5000');

        textareaMarker.addEventListener('input', function (evt) {
            window.zones.get(textareaMarker.id.substring(7)).marker_name = textareaMarker.value;
            draw_figures();
        });

        window.zones.get(textareaMarker.id.substring(7)).zoneType.addEventListener('change', function (evt) {
            selectedOption = window.zones.get(textareaMarker.id.substring(7)).zoneType.options[window.zones.get(textareaMarker.id.substring(7)).zoneType.selectedIndex];
            if(selectedOption.getAttribute('key') === "polygon") {
                window.zones.set(textareaMarker.id.substring(7), {vertexes:[{x:10,y:10,v:false},{x:10,y:60,v:false},{x:60,y:60,v:false},{x:60,y:10,v:false}],isDragging:false,selected:false,zoneType:window.zones.get(textareaMarker.id.substring(7)).zoneType, marker_name:textareaMarker.value, textareaCoords:window.zones.get(textareaMarker.id.substring(7)).textareaCoords});
            }else if(selectedOption.getAttribute('key') === "circle") {
                window.zones.set(textareaMarker.id.substring(7), {x:60,y:60,radius:40,isDragging:false,selected:false,zoneType:window.zones.get(textareaMarker.id.substring(7)).zoneType, marker_name:textareaMarker.value, textareaCoords:window.zones.get(textareaMarker.id.substring(7)).textareaCoords});
            }
            draw_figures();
        });

        window.zones.get(textareaMarker.id.substring(7)).textareaCoords.addEventListener('input', function (evt) {
            let string = window.zones.get(textareaMarker.id.substring(7)).textareaCoords.value;

            selectedOption = window.zones.get(textareaMarker.id.substring(7)).zoneType.options[window.zones.get(textareaMarker.id.substring(7)).zoneType.selectedIndex];
            if(selectedOption.getAttribute('key') === "polygon") {
                let coordsAmount = window.zones.get(textareaMarker.id.substring(7)).textareaCoords.value.match(/;/g).length;
                let delimiter, coords, comma;
                window.zones.get(window.zones.get(textareaMarker.id.substring(7)).textareaCoords.id.substring(12)).vertexes = []
                for(let i = 0; i < coordsAmount; i++){
                    if(i > 0){
                        delimiter = string.indexOf(";");
                        string = string.slice(delimiter+1);
                    }
                    delimiter = string.indexOf(";");
                    if(delimiter > 0)
                        coords = string.slice(0, delimiter);
                    else
                        coords = string
                    comma = coords.indexOf(",");
                    let new_x = parseInt(coords.slice(0, comma));
                    let new_y = parseInt(coords.slice(comma+1));
                    window.zones.get(window.zones.get(textareaMarker.id.substring(7)).textareaCoords.id.substring(12)).vertexes.push({x:new_x, y: new_y, v:false})
                }
            } else if(selectedOption.getAttribute('key') === "circle") {
                let circle = window.zones.get(window.zones.get(textareaMarker.id.substring(7)).textareaCoords.id.substring(12));
                let delimiter = string.indexOf(",");
                circle.x = parseInt(string.slice(0, delimiter));
                string = string.slice(delimiter+1);
                delimiter = string.indexOf(",");
                circle.y = parseInt(string.slice(0, delimiter));
                string = string.slice(delimiter+1);
                circle.radius = parseInt(string);
            }
            draw_figures(false);
        });

        draw_figures();
    }

    let textareaQuestionCom, comDiv;
    if(selectedOption.getAttribute('key') === "compliance") {
        textareaQuestionCom = document.createElement('textarea');
        comDiv = document.createElement('div');
        textareaQuestionCom.setAttribute('class', "form-control langp");
        textareaQuestionCom.setAttribute('key', "question_text");
        textareaQuestionCom.setAttribute('placeholder', "Текст вопроса");
        textareaQuestionCom.setAttribute('name', "QuestionCom-" + questionIndex + "-" + answerIndex);
        textareaQuestionCom.setAttribute('rows', "1");
        textareaQuestionCom.setAttribute('maxlength', '5000');
        comDiv.textContent = "-";
        comDiv.setAttribute('style', "margin-left: 5px; margin-right: 5px;");
    }

    let optionDiv, optionText, optionNumText, groupDiv, groupSelect;
    if(selectedOption.getAttribute('key') === "filling_gaps" || selectedOption.getAttribute('key') === "drag_to_text") {
        optionDiv = document.createElement('div');
        optionDiv.setAttribute('style', "width: 147px;");
        optionText = document.createElement('text');
        optionText.setAttribute('class', "lang");
        optionText.setAttribute('key', "option");
        optionText.textContent = "Вариант"
        optionNumText = document.createElement('text');
        optionNumText.textContent = " [[" + answerIndex + "]]"
        if (selectedOption.getAttribute('key') === "filling_gaps") {
            groupDiv = document.createElement('div');
            groupDiv.setAttribute('style', "width: 70px; margin-left: 8px; margin-right: 4px;");
            groupDiv.setAttribute('class', "lang");
            groupDiv.setAttribute('key', "group_");
            groupDiv.textContent = "Группа";
            groupSelect = document.createElement('select');
            groupSelect.setAttribute('class', "form-select");
            groupSelect.setAttribute('style', "width: 60px;");
            groupSelect.setAttribute('name', "Group-" + questionIndex + "-" + answerIndex);
            let alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
            alphabet.forEach(elem => {
                let option = document.createElement('option');
                option.textContent = elem;
                groupSelect.appendChild(option);
            })
        }
    }

    let textarea = document.createElement('textarea');
    textarea.setAttribute('class', "form-control langp");
    textarea.setAttribute('key', "answer_text");
    textarea.setAttribute('maxlength', '5000');
    textarea.setAttribute('placeholder', "Текст ответа");
    textarea.setAttribute('name', `Answer-${index.substring(7)}-${answerIndex}`);
    textarea.setAttribute('rows', "1");

    let label, input;
    if(selectedOption.getAttribute('key') === "solo" || selectedOption.getAttribute('key') === "multiple") {
        label = document.createElement('label');
        input = document.createElement('input');
        label.setAttribute('for', "addAnswerText");
        label.setAttribute('style', "padding-right: 8px;");
        //input.setAttribute('required', 'true');
        if (selectedOption.getAttribute('key') === "solo") {
            input.setAttribute("type", "radio");
            input.setAttribute('name', `Right_Answer-${index.substring(7)}`);
        }
        if (selectedOption.getAttribute('key') === "multiple") {
            input.setAttribute("type", "checkbox");
            input.setAttribute('name', `Right_Answer-${index.substring(7)}-${answerIndex}`);
        }
    }

    let buttonDel = document.createElement('button');
    buttonDel.setAttribute('class', "btn");
    buttonDel.setAttribute('style', "background-color:red; color:white; padding: 4px; width: 25px;");
    buttonDel.setAttribute('onclick', "deleteElement(\"delAns-\" + this.id); window.zones.delete(this.name + \"-\" + this.id); window.draw_figures();");
    buttonDel.textContent = "✖"
    buttonDel.setAttribute('id', answerIndex);
    buttonDel.setAttribute('name', parseInt(index.substring(7)) + 1);
    let divDel = document.createElement('div');
    divDel.setAttribute('style', "padding-left: 5px;");

    let divAnsCard = addDragndropDesign(div, 'answer')

    if(selectedOption.getAttribute('key') === "solo" || selectedOption.getAttribute('key') === "multiple") {
        label.appendChild(input)
        div.appendChild(label)
        div.appendChild(textarea)
    } else if(selectedOption.getAttribute('key') === "compliance"){
        div.appendChild(textareaQuestionCom)
        div.appendChild(comDiv)
        div.appendChild(textarea)
    } else if(selectedOption.getAttribute('key') === "filling_gaps" || selectedOption.getAttribute('key') === "drag_to_text"){
        optionDiv.appendChild(optionText)
        optionDiv.appendChild(optionNumText)
        div.appendChild(optionDiv)
        div.appendChild(textarea)
        if (selectedOption.getAttribute('key') === "filling_gaps") {
            div.appendChild(groupDiv)
            div.appendChild(groupSelect)
        }
    } else if (selectedOption.getAttribute('key') === "markers_drag") {
        div.appendChild(divMarker)
        div.appendChild(textareaMarker)
        div.appendChild(divZone)
        div.appendChild(window.zones.get(textareaMarker.id.substring(7)).zoneType)
        window.zones.get(textareaMarker.id.substring(7)).zoneType.appendChild(polygon)
        window.zones.get(textareaMarker.id.substring(7)).zoneType.appendChild(circleVis)
        div.appendChild(divCoords)
        div.appendChild(window.zones.get(textareaMarker.id.substring(7)).textareaCoords)
    }
    divDel.appendChild(buttonDel)
    div.appendChild(divDel)
    div.appendChild(divAnsCard)
    let answersElm = document.getElementById(index);
    answersElm.appendChild(div);

    answerIndex += 1;
    let lang = localStorage.getItem('language');
    translate(lang);
};

window.deleteElement = function(index){
    document.getElementById(index).remove()
};

// Функция добавления области перетаскивания
export function addDragndropDesign(div, type) {
    let divDragCard = document.createElement('div');
    let dragImg = document.createElement('img');
    dragImg.setAttribute('src', "/static/img/drag_n_drop.png");
    divDragCard.setAttribute('draggable', "True");
    if(type === 'question'){
        divDragCard.setAttribute('style', "height: 35px; justify-content: center; display: flex;");
        dragImg.setAttribute('style', "height: 35px;");
    } else if(type === 'answer'){
        divDragCard.setAttribute('style', "height: 30px; justify-content: center; display: flex;");
        dragImg.setAttribute('style', "height: 30px; transform: rotate(90deg);");
    }
    divDragCard.appendChild(dragImg)

    addDragndropDesignVoid(div, divDragCard, type)
    return divDragCard;
}

// Функция настройки области перетаскивания
export function addDragndropDesignVoid(div, divDragCard, type) {
    divDragCard.addEventListener(`mouseover`, (evt) => {
      document.body.style.cursor = 'move';
    })
    divDragCard.addEventListener(`mouseout`, (evt) => {
      document.body.style.cursor = '';
    })
    divDragCard.addEventListener(`dragstart`, (evt) => {
      if(type === 'question'){
          evt.dataTransfer.setDragImage(div, div.offsetWidth / 1.78, div.offsetHeight / 18)
      } else if(type === 'answer'){
          evt.dataTransfer.setDragImage(div, div.offsetWidth / 1.032, div.offsetHeight / 2)
      } else if(type === 'editor'){
          evt.dataTransfer.setDragImage(div[parseInt(evt.target.className) - 1], div[parseInt(evt.target.className) - 1].offsetWidth / 1.78, div[parseInt(evt.target.className) - 1].offsetHeight / 18)
          setTimeout(() => {
              div[parseInt(evt.target.className) - 1].classList.add(`selected`);
              div[parseInt(evt.target.className) - 1].style.visibility  = "hidden"
          }, 0);
      } else if(type === 'course'){
          evt.dataTransfer.setDragImage(div, div.offsetWidth / 1.92, div.offsetHeight / 8)
      } else if(type === 'unit'){
          evt.dataTransfer.setDragImage(div, div.offsetWidth / 1.09, div.offsetHeight / 8)
      }
      if(type !== 'editor') {
          setTimeout(() => {
              div.classList.add(`selected`);
              div.style.visibility = "hidden"
          }, 0);
      }
    })
    divDragCard.addEventListener(`dragend`, (evt) => {
      if(type !== 'editor') {
          setTimeout(() => {
              div.classList.remove(`selected`);
              div.style.removeProperty("visibility")
          }, 0);
      } else if(type === 'editor'){
          setTimeout(() => {
              div[parseInt(evt.target.className) - 1].classList.remove(`selected`);
              div[parseInt(evt.target.className) - 1].style.removeProperty("visibility")
          }, 0);
      }
    });
}

// Добавление нового вопроса
export function addQuestionListener(addBtn) {
    addBtn.addEventListener("click", function (e) {
        // Внешний div
        let div = document.createElement('div');
        div.setAttribute('id', "delQue-" + questionIndex);
        div.setAttribute('class', "question_div");
        // Карточка вопроса
        let divCard = document.createElement('div');
        divCard.setAttribute('class', "card");

        // Drag'n'drop область
        let divDragCard = addDragndropDesign(div, 'question');

        let divCardBody = document.createElement('div');
        divCardBody.setAttribute('class', "card-body");
        let formGroup = document.createElement('div');
        formGroup.setAttribute('class', "form-group");
        // Содержимое карточки
        let textareaQuestion = document.createElement('textarea');
        textareaQuestion.setAttribute('class', "form-control langp");
        textareaQuestion.setAttribute('key', "question_text");
        textareaQuestion.setAttribute('placeholder', "Текст вопроса");
        textareaQuestion.setAttribute('id', "question");
        textareaQuestion.setAttribute('rows', "1");
        textareaQuestion.setAttribute('required', 'true');
        textareaQuestion.setAttribute('maxlength', '5000');
        textareaQuestion.setAttribute('name', 'Question-' + questionIndex);
        let hr = document.createElement('hr');
        let divIndex = document.createElement('div');
        divIndex.setAttribute('class', "row container-fluid");
        divIndex.setAttribute('id', "addAns-" + questionIndex);
        let divTextLabel = document.createElement('div');
        divTextLabel.setAttribute('style', "padding-bottom: 10px; display: flex; align-items: center;");
        divTextLabel.setAttribute('id', "delAns-" + answerIndex);
        divTextLabel.setAttribute('class', "answer_div");
        let textareaAnswer = document.createElement('textarea');
        textareaAnswer.setAttribute('class', "form-control langp");
        textareaAnswer.setAttribute('key', "answer_text");
        textareaAnswer.setAttribute('placeholder', "Текст ответа");
        textareaAnswer.setAttribute('name', "Answer-" + questionIndex + "-" + answerIndex);
        textareaAnswer.setAttribute('rows', "1");
        textareaAnswer.setAttribute('maxlength', '5000');
        textareaAnswer.setAttribute('required', 'true');
        let label = document.createElement('label');
        label.setAttribute('for', "addAnswerText");
        label.setAttribute('style', "padding-right: 8px;");
        let input = document.createElement('input');
        input.setAttribute('type', "radio");
        let br = document.createElement('br');
        let button = document.createElement('button');
        button.setAttribute('class', "btn lang");
        button.setAttribute('style', "background-color:transparent; color:black;");
        button.setAttribute('onclick', "addAnswerOnButtonClick(\"addAns-\" + this.id)");
        button.textContent = "Добавить ответ"
        button.setAttribute('key', "add_answer");
        button.setAttribute('id', questionIndex);
        button.setAttribute('type', "button");
        input.setAttribute('name', "Right_Answer-" + questionIndex);
        let buttonDelQuestion = document.createElement('button');
        buttonDelQuestion.setAttribute('class', "btn lang");
        buttonDelQuestion.setAttribute('type', "button");
        buttonDelQuestion.setAttribute('style', "background-color:red; color:white;");
        buttonDelQuestion.setAttribute('onclick', "deleteElement(\"delQue-\" + this.id)");
        buttonDelQuestion.textContent = "Удалить вопрос"
        buttonDelQuestion.setAttribute('key', "delete_answer");
        buttonDelQuestion.setAttribute('id', questionIndex);
        let buttonUpQuestion = document.createElement('button');
        buttonUpQuestion.setAttribute('type', "button");
        buttonUpQuestion.setAttribute('class', "btn");
        buttonUpQuestion.setAttribute('style', "background-color:white; color:black; padding: 4px; width: 35px; height: 35px; font-size:20px;");
        buttonUpQuestion.addEventListener("click", function () {
            let questionsList = document.getElementById("questionsList");
            questionsList.insertBefore(div, div.previousElementSibling);
        });
        buttonUpQuestion.textContent = "↑"
        let buttonDownQuestion = document.createElement('button');
        buttonDownQuestion.setAttribute('type', "button");
        buttonDownQuestion.setAttribute('class', "btn");
        buttonDownQuestion.setAttribute('style', "background-color:white; color:black; padding: 4px; width: 35px; height: 35px; font-size:20px;");
        buttonDownQuestion.addEventListener("click", function () {
            let questionsList = document.getElementById("questionsList");
            if (div.nextElementSibling == null) {
                questionsList.insertBefore(div, questionsList.firstChild);
            } else {
                questionsList.insertBefore(div.nextElementSibling, div);
            }
        });
        buttonDownQuestion.textContent = "↓"
        let buttonDel = document.createElement('button');
        buttonDel.setAttribute('class', "btn");
        buttonDel.setAttribute('style', "background-color:red; color:white; padding: 4px; width: 25px;");
        buttonDel.setAttribute('onclick', "deleteElement(\"delAns-\" + this.id)");
        buttonDel.textContent = "✖"
        buttonDel.setAttribute('id', answerIndex);
        let divDel = document.createElement('div');
        divDel.setAttribute('style', "padding-left: 5px;");

        addDragoverEventListener(divIndex, `answer_div`);
        let divAnsCard = addDragndropDesign(divTextLabel, 'answer');

        let div_shuffle = document.createElement('div');
        div_shuffle.setAttribute('class', "to_del");
        let text_shuffle = document.createElement('text');
        text_shuffle.setAttribute('class', "lang");
        text_shuffle.setAttribute('key', "shuffle");
        text_shuffle.textContent = "Перемешивать варианты ответов между собой";
        let label_for_shuffle = document.createElement('label');
        label_for_shuffle.setAttribute('for', "Shuffle-" + questionIndex);
        label_for_shuffle.setAttribute('style', "padding-right: 8px;");
        let input_shuffle = document.createElement('input');
        input_shuffle.setAttribute('style', "margin-right: 10px; margin-top: 12px;");
        input_shuffle.setAttribute('type', "checkbox");
        input_shuffle.setAttribute('name', "Shuffle-" + questionIndex);
        label_for_shuffle.appendChild(text_shuffle)
        div_shuffle.appendChild(input_shuffle)
        div_shuffle.appendChild(label_for_shuffle)

        let questionType = document.createElement('select')
        questionType.setAttribute('class', "form-select");
        questionType.setAttribute('width', "20px");
        questionType.setAttribute('id', "QT-" + questionIndex);
        questionType.setAttribute('name', "QuestionType-" + questionIndex);
        let radio = document.createElement('option')
        radio.setAttribute('class', "lang");
        radio.setAttribute('key', "solo");
        radio.textContent = "Единственный ответ"
        let check = document.createElement('option')
        check.setAttribute('class', "lang");
        check.setAttribute('key', "multiple");
        check.textContent = "Множественный ответ"
        let compliance = document.createElement('option')
        compliance.setAttribute('class', "lang");
        compliance.setAttribute('key', "compliance");
        compliance.textContent = "На соответствие"
        let filling_gaps = document.createElement('option')
        filling_gaps.setAttribute('class', "lang");
        filling_gaps.setAttribute('key', "filling_gaps");
        filling_gaps.textContent = "Заполнение пропусков"
        let drag_to_text = document.createElement('option')
        drag_to_text.setAttribute('class', "lang");
        drag_to_text.setAttribute('key', "drag_to_text");
        drag_to_text.textContent = "Перетаскивание в текст"
        let markers_drag = document.createElement('option')
        markers_drag.setAttribute('class', "lang");
        markers_drag.setAttribute('key', "markers_drag");
        markers_drag.textContent = "Перетаскивание маркеров"
        let word = document.createElement('option')
        word.setAttribute('class', "lang");
        word.setAttribute('key', "free");
        word.textContent = "Краткий свободный ответ"
        let text = document.createElement('option')
        text.setAttribute('class', "lang");
        text.setAttribute('key', "detailed_free");
        text.textContent = "Свободный ответ"
        let info = document.createElement('option')
        info.setAttribute('class', "lang");
        info.setAttribute('key', "info_block");
        info.textContent = "Информационный блок"
        let divController = document.createElement('div');
        divController.setAttribute('style', "display: flex;");
        let divBT = document.createElement('div');
        divBT.setAttribute('style', "padding-left: 5px;");
        let divDQ = document.createElement('div');
        divDQ.setAttribute('style', "padding-left: 5px;");
        let divUP = document.createElement('div');
        divUP.setAttribute('style', "padding-left: 5px;");
        let divDW = document.createElement('div');
        divDW.setAttribute('style', "padding-left: 5px;");
        let divQT = document.createElement('div');
        divQT.setAttribute('style', "width: 280px; padding-left: 5px;");
        questionType.appendChild(radio)
        questionType.appendChild(check)
        questionType.appendChild(compliance)
        questionType.appendChild(filling_gaps)
        questionType.appendChild(drag_to_text)
        questionType.appendChild(markers_drag)
        questionType.appendChild(word)
        questionType.appendChild(text)
        questionType.appendChild(info)
        questionTypeSet(questionType, textareaQuestion, button.id)

        // Навигационная карточка
        let divQueCard = document.createElement('div');
        divQueCard.setAttribute('class', "card");
        divQueCard.setAttribute('style', "background:#d9d9d9; height: 120px; margin-right: 10px;");
        divCard.setAttribute('style', "background:#bde0ff; flex: 1;");
        div.setAttribute('style', "display: flex; padding-bottom: 20px;");
        let divQueCardBody = document.createElement('div');
        divQueCardBody.setAttribute('class', "card-body");
        let formQueGroup = document.createElement('div');
        formQueGroup.setAttribute('class', "form-group");
        let question = document.createElement('p');
        let question_txt = document.createElement('text');
        question_txt.setAttribute('class', "lang");
        question_txt.setAttribute('key', "question");
        question_txt.textContent = "Вопрос"
        let question_txt1 = document.createElement('text');
        question_txt1.textContent = " №" + questionIndex
        question.appendChild(question_txt);
        question.appendChild(question_txt1);
        let inputScore = document.createElement('input');
        inputScore.setAttribute('type', "number");
        inputScore.setAttribute('name', "score-" + questionIndex);
        inputScore.setAttribute('required', 'true');
        inputScore.setAttribute('style', 'width:40px;');
        inputScore.setAttribute('maxlength', '10');
        inputScore.value = 1
        let labelScore = document.createElement('label');
        labelScore.setAttribute('for', "score-" + questionIndex);
        labelScore.setAttribute('class', "lang");
        labelScore.setAttribute('key', "score");
        labelScore.textContent = "Баллы: "

        div.appendChild(divQueCard)
        divQueCard.appendChild(divQueCardBody)
        divQueCardBody.appendChild(formQueGroup)
        formQueGroup.appendChild(question)
        formQueGroup.appendChild(labelScore)
        formQueGroup.appendChild(inputScore)

        // Создание всей этой позорной иерархии
        div.appendChild(divCard)
        divCard.appendChild(divDragCard)
        divCard.appendChild(divCardBody)
        divCardBody.appendChild(formGroup)
        formGroup.appendChild(textareaQuestion)
        formGroup.appendChild(hr)
        formGroup.appendChild(divIndex)
        divIndex.appendChild(divTextLabel)
        label.appendChild(input)
        divTextLabel.appendChild(label)
        divTextLabel.appendChild(textareaAnswer)
        divDel.appendChild(buttonDel)
        divTextLabel.appendChild(divDel)
        divTextLabel.appendChild(divAnsCard)
        formGroup.appendChild(br)
        divBT.appendChild(button)
        divController.appendChild(divBT)
        divDQ.appendChild(buttonDelQuestion)
        divUP.appendChild(buttonUpQuestion)
        divDW.appendChild(buttonDownQuestion)
        divController.appendChild(divDQ)
        divQT.appendChild(questionType)
        divController.appendChild(divQT)
        divController.appendChild(divUP)
        divController.appendChild(divDW)
        formGroup.appendChild(divController)
        formGroup.insertBefore(div_shuffle, br)

        let answersElm = document.getElementById("questionsList");
        answersElm.appendChild(div)

        questionIndex += 1;
        answerIndex += 1;

        let lang = localStorage.getItem('language');
        translate(lang);
    });
}

window.zones  = new Map();

// Функция настройки смены типа задания при его выборе через выпадающий список
export function questionTypeSet(questionType, textareaQuestion, questionIndexButtonId) {
    questionType.addEventListener("change", function () {

        $(".to_del", $(textareaQuestion).parent("div:first")).each  (function (){
            this.remove();
        });

        let selectedOption = questionType.options[questionType.selectedIndex];

        let div_shuffle, text_shuffle, label_for_shuffle, input_shuffle;
        if (["solo", "multiple", "compliance", "filling_gaps", "drag_to_text", "markers_drag"].indexOf(selectedOption.getAttribute('key')) !== -1) {
            div_shuffle = document.createElement('div');
            div_shuffle.setAttribute('class', "to_del");
            text_shuffle = document.createElement('text');
            text_shuffle.setAttribute('class', "lang");
            text_shuffle.setAttribute('key', "shuffle");
            text_shuffle.textContent = "Перемешивать варианты ответов между собой";
            label_for_shuffle = document.createElement('label');
            label_for_shuffle.setAttribute('for', "Shuffle-" + questionIndex);
            label_for_shuffle.setAttribute('style', "padding-right: 8px;");
            input_shuffle = document.createElement('input');
            input_shuffle.setAttribute('style', "margin-right: 10px; margin-top: 12px;");
            input_shuffle.setAttribute('type', "checkbox");
            input_shuffle.setAttribute('name', "Shuffle-" + questionIndex);
            label_for_shuffle.appendChild(text_shuffle)
            div_shuffle.appendChild(input_shuffle)
            div_shuffle.appendChild(label_for_shuffle)
        }

        if (selectedOption.getAttribute('key') === "solo" || selectedOption.getAttribute('key') === "multiple") {
            textareaQuestion.setAttribute('rows', "1");
            let divIndexNew = document.createElement('div');
            divIndexNew.setAttribute('class', "row container-fluid");
            divIndexNew.setAttribute('id', "addAns-" + questionIndexButtonId);
            let divTextLabel = document.createElement('div');
            divTextLabel.setAttribute('style', "padding-bottom: 10px; display: flex; align-items: center;");
            divTextLabel.setAttribute('id', "delAns-" + answerIndex);
            divTextLabel.setAttribute('class', "answer_div");
            let textareaAnswer = document.createElement('textarea');
            textareaAnswer.setAttribute('class', "form-control langp");
            textareaAnswer.setAttribute('key', "answer_text");
            textareaAnswer.setAttribute('placeholder', "Текст ответа");
            textareaAnswer.setAttribute('name', "Answer-" + questionIndex + "-" + answerIndex);
            textareaAnswer.setAttribute('rows', "1");
            textareaAnswer.setAttribute('maxlength', '5000');
            let label = document.createElement('label');
            label.setAttribute('for', "addAnswerText");
            label.setAttribute('style', "padding-right: 8px;");
            let input = document.createElement('input');
            //input.setAttribute('required', 'true');
            if (selectedOption.getAttribute('key') === "solo") {
                input.setAttribute('type', "radio");
                input.setAttribute('name', "Right_Answer-" + questionIndexButtonId);
            }
            if (selectedOption.getAttribute('key') === "multiple") {
                input.setAttribute('type', "checkbox");
                input.setAttribute('name', "Right_Answer-" + questionIndexButtonId + "-" + answerIndex);
            }
            let buttonDel = document.createElement('button');
            buttonDel.setAttribute('class', "btn");
            buttonDel.setAttribute('style', "background-color:red; color:white; padding: 4px; width: 25px;");
            buttonDel.setAttribute('onclick', "deleteElement(\"delAns-\" + this.id)");
            buttonDel.textContent = "✖"
            buttonDel.setAttribute('id', answerIndex);
            let divDel = document.createElement('div');
            divDel.setAttribute('style', "padding-left: 5px;");

            addDragoverEventListener(divIndexNew, `answer_div`);
            let divAnsCard = addDragndropDesign(divTextLabel, 'answer');

            divIndexNew.appendChild(divTextLabel)
            label.appendChild(input)
            divTextLabel.appendChild(label)
            divTextLabel.appendChild(textareaAnswer)
            divDel.appendChild(buttonDel)
            divTextLabel.appendChild(divDel)
            divTextLabel.appendChild(divAnsCard)
            let divIndexTmp = document.getElementById("addAns-" + questionIndexButtonId)
            divIndexTmp.replaceWith(divIndexNew);
            divIndexNew.parentElement.insertBefore(div_shuffle, divIndexNew.nextElementSibling)
            let buttonNew = document.getElementById(questionIndexButtonId)
            buttonNew.removeAttribute("disabled");
        }
        if (selectedOption.getAttribute('key') === "compliance"){
            textareaQuestion.setAttribute('rows', "1");
            let divIndexNew = document.createElement('div');
            divIndexNew.setAttribute('class', "row container-fluid");
            divIndexNew.setAttribute('id', "addAns-" + questionIndexButtonId);
            let divTextLabel = document.createElement('div');
            divTextLabel.setAttribute('style', "padding-bottom: 10px; display: flex; align-items: center;");
            divTextLabel.setAttribute('id', "delAns-" + answerIndex);
            divTextLabel.setAttribute('class', "answer_div");
            let textareaQuestionCom = document.createElement('textarea');
            textareaQuestionCom.setAttribute('class', "form-control langp");
            textareaQuestionCom.setAttribute('key', "question_text");
            textareaQuestionCom.setAttribute('placeholder', "Текст вопроса");
            textareaQuestionCom.setAttribute('name', "QuestionCom-" + questionIndex + "-" + answerIndex);
            textareaQuestionCom.setAttribute('rows', "1");
            textareaQuestionCom.setAttribute('maxlength', '5000');
            let comDiv = document.createElement('div');
            comDiv.textContent = "-";
            comDiv.setAttribute('style', "margin-left: 5px; margin-right: 5px;");
            let textareaAnswer = document.createElement('textarea');
            textareaAnswer.setAttribute('class', "form-control langp");
            textareaAnswer.setAttribute('key', "answer_text");
            textareaAnswer.setAttribute('placeholder', "Текст ответа");
            textareaAnswer.setAttribute('name', "Answer-" + questionIndex + "-" + answerIndex);
            textareaAnswer.setAttribute('rows', "1");
            textareaAnswer.setAttribute('maxlength', '5000');

            let buttonDel = document.createElement('button');
            buttonDel.setAttribute('class', "btn");
            buttonDel.setAttribute('style', "background-color:red; color:white; padding: 4px; width: 25px;");
            buttonDel.setAttribute('onclick', "deleteElement(\"delAns-\" + this.id)");
            buttonDel.textContent = "✖"
            buttonDel.setAttribute('id', answerIndex);
            let divDel = document.createElement('div');
            divDel.setAttribute('style', "padding-left: 5px;");

            addDragoverEventListener(divIndexNew, `answer_div`);
            let divAnsCard = addDragndropDesign(divTextLabel, 'answer');

            let comNote = document.createElement('div');
            comNote.setAttribute('style', "color: gray; font-size: 14px;");
            comNote.setAttribute('class', "to_del lang");
            comNote.setAttribute('key', "compliance_note");
            comNote.textContent = "*Примечание: если вы хотите добавить неверный ответ, то для пары вопрос-ответ поле с вопросом необходимо оставить пустым";

            divIndexNew.appendChild(divTextLabel)
            divTextLabel.appendChild(textareaQuestionCom)
            divTextLabel.appendChild(comDiv)
            divTextLabel.appendChild(textareaAnswer)
            divDel.appendChild(buttonDel)
            divTextLabel.appendChild(divDel)
            divTextLabel.appendChild(divAnsCard)
            let divIndexTmp = document.getElementById("addAns-" + questionIndexButtonId)
            divIndexTmp.replaceWith(divIndexNew);
            divIndexNew.parentElement.insertBefore(comNote, divIndexNew.nextElementSibling)
            divIndexNew.parentElement.insertBefore(div_shuffle, comNote)
            let buttonNew = document.getElementById(questionIndexButtonId)
            buttonNew.removeAttribute("disabled");
        }
        if (selectedOption.getAttribute('key') === "filling_gaps" || selectedOption.getAttribute('key') === "drag_to_text") {
            textareaQuestion.setAttribute('rows', "8");
            let divIndexNew = document.createElement('div');
            divIndexNew.setAttribute('class', "row container-fluid");
            divIndexNew.setAttribute('id', "addAns-" + questionIndexButtonId);
            let divTextLabel = document.createElement('div');
            divTextLabel.setAttribute('style', "padding-bottom: 10px; display: flex; align-items: center;");
            divTextLabel.setAttribute('id', "delAns-" + answerIndex);
            divTextLabel.setAttribute('class', "answer_div");
            let optionDiv = document.createElement('div');
            optionDiv.setAttribute('style', "width: 147px;");
            let optionText = document.createElement('text');
            optionText.setAttribute('class', "lang");
            optionText.setAttribute('key', "option");
            optionText.textContent = "Вариант"
            let optionNumText = document.createElement('text');
            optionNumText.textContent = " [[1]]"
            let textareaAnswer = document.createElement('textarea');
            textareaAnswer.setAttribute('class', "form-control langp");
            textareaAnswer.setAttribute('key', "answer_text");
            textareaAnswer.setAttribute('placeholder', "Текст ответа");
            textareaAnswer.setAttribute('name', "Answer-" + questionIndex + "-" + answerIndex);
            textareaAnswer.setAttribute('rows', "1");
            textareaAnswer.setAttribute('maxlength', '5000');
            let groupDiv;
            let groupSelect;
            if (selectedOption.getAttribute('key') === "filling_gaps") {
                groupDiv = document.createElement('div');
                groupDiv.setAttribute('style', "width: 70px; margin-left: 8px; margin-right: 4px;");
                groupDiv.setAttribute('class', "lang");
                groupDiv.setAttribute('key', "group_");
                groupDiv.textContent = "Группа";
                groupSelect = document.createElement('select');
                groupSelect.setAttribute('class', "form-select");
                groupSelect.setAttribute('style', "width: 60px;");
                groupSelect.setAttribute('name', "Group-" + questionIndex + "-" + answerIndex);
                let alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
                alphabet.forEach(elem => {
                    let option = document.createElement('option');
                    option.textContent = elem;
                    groupSelect.appendChild(option);
                })
            }
            let buttonDel = document.createElement('button');
            buttonDel.setAttribute('class', "btn");
            buttonDel.setAttribute('style', "background-color:red; color:white; padding: 4px; width: 25px;");
            buttonDel.setAttribute('onclick', "deleteElement(\"delAns-\" + this.id)");
            buttonDel.textContent = "✖"
            buttonDel.setAttribute('id', answerIndex);
            let divDel = document.createElement('div');
            divDel.setAttribute('style', "padding-left: 5px;");

            addDragoverEventListener(divIndexNew, `answer_div`);
            let divAnsCard = addDragndropDesign(divTextLabel, 'answer');

            let fillNote = document.createElement('div');
            fillNote.setAttribute('style', "color: gray; font-size: 14px;");
            fillNote.setAttribute('class', "to_del lang");
            fillNote.setAttribute('key', "filling_gaps_note");
            fillNote.textContent = "*Примечание: текст вопроса должен содержать метки-заполнители, например [[1]], для обозначения местонахождения пропущенных слов";

            divIndexNew.appendChild(divTextLabel)
            optionDiv.appendChild(optionText)
            optionDiv.appendChild(optionNumText)
            divTextLabel.appendChild(optionDiv)
            divTextLabel.appendChild(textareaAnswer)
            if (selectedOption.getAttribute('key') === "filling_gaps") {
                divTextLabel.appendChild(groupDiv)
                divTextLabel.appendChild(groupSelect)
            }
            divDel.appendChild(buttonDel)
            divTextLabel.appendChild(divDel)
            divTextLabel.appendChild(divAnsCard)
            let divIndexTmp = document.getElementById("addAns-" + questionIndexButtonId)
            divIndexTmp.replaceWith(divIndexNew);
            divIndexNew.parentElement.insertBefore(fillNote, divIndexNew.nextElementSibling)
            divIndexNew.parentElement.insertBefore(div_shuffle, fillNote)
            let buttonNew = document.getElementById(questionIndexButtonId)
            buttonNew.removeAttribute("disabled");
        }
        if (selectedOption.getAttribute('key') === "markers_drag"){
            window.zones.set(questionIndex + "-" + answerIndex, {vertexes:[{x:10,y:10,v:false},{x:10,y:60,v:false},{x:60,y:60,v:false},{x:60,y:10,v:false}],isDragging:false,selected:false});

            textareaQuestion.setAttribute('rows', "1");
            let span = document.createElement('span');
            span.setAttribute('class', "fs-5 row m-3 justify-content-start to_del");
            let divFlex = document.createElement('div');
            divFlex.setAttribute('class', "flex-column");
            let divCanv = document.createElement('div');
            divCanv.setAttribute('style', "height: 586px; overflow-y: hidden; overflow-x: visible");
            divCanv.setAttribute('id', "canvasContainer" + questionIndexButtonId);
            let canvas = document.createElement('canvas');
            canvas.setAttribute('id', "canvas-" + questionIndexButtonId);
            canvas.setAttribute('width', "1036px");
            canvas.setAttribute('height', "9999px");
            canvas.setAttribute('style', "border:1px solid red; background-repeat: repeat; background-position: 0 0; background-image: url(\"/static/img/nophoto.png\"");
            let form = document.createElement('form');
            form.setAttribute('method', "POST");
            form.setAttribute('enctype', "multipart/form-data");
            form.setAttribute('style', "max-width: 290px; margin: 0 auto;");
            let inputFile = document.createElement('input');
            inputFile.setAttribute('type', "file");
            inputFile.setAttribute('name', "File-" + questionIndexButtonId);
            inputFile.setAttribute('id', "File-" + questionIndexButtonId);
            inputFile.setAttribute('class', "form-control");
            let aForButton = document.createElement('a');
            let aButton = document.createElement('Button');
            aButton.setAttribute('class', "btn border border-2 w-100 lang");
            aButton.setAttribute('key', "add_background_image");
            aButton.setAttribute('id', "addBackgroundImage");
            aButton.setAttribute('type', "button");
            aButton.setAttribute('textContent', "Добавить фоновое изображение");
            let divIndexNew = document.createElement('div');
            divIndexNew.setAttribute('class', "row container-fluid");
            divIndexNew.setAttribute('id', "addAns-" + questionIndexButtonId);
            let divTextLabel = document.createElement('div');
            divTextLabel.setAttribute('style', "padding-bottom: 10px; display: flex; align-items: center;");
            divTextLabel.setAttribute('id', "delAns-" + answerIndex);
            divTextLabel.setAttribute('class', "answer_div");
            let divMarker = document.createElement('div');
            divMarker.setAttribute('style', "width: 75px; margin-right: 4px;");
            divMarker.setAttribute('key', "marker");
            divMarker.setAttribute('class', "lang");
            divMarker.textContent = "Маркер";
            let textareaMarker = document.createElement('textarea');
            textareaMarker.setAttribute('class', "form-control langp");
            textareaMarker.setAttribute('key', "marker_name");
            textareaMarker.setAttribute('placeholder', "Название маркера");
            textareaMarker.setAttribute('name', "Marker-" + questionIndex + "-" + answerIndex);
            textareaMarker.setAttribute('id', "Marker-" + questionIndex + "-" + answerIndex);
            textareaMarker.setAttribute('rows', "1");
            textareaMarker.setAttribute('maxlength', '5000');
            let divZone = document.createElement('div');
            divZone.setAttribute('style', "width: 450px; margin-left: 8px; margin-right: 2px;");
            divZone.setAttribute('key', "zone_type");
            divZone.setAttribute('class', "lang");
            divZone.textContent = "Форма зоны";
            // let zoneType = document.createElement('select')
            //window.zones.set(questionIndex + "-" + answerIndex, window.zones.get(textareaMarker.id.substring(7)).zoneType = document.createElement('select'))
            window.zones.get(textareaMarker.id.substring(7)).zoneType = document.createElement('select')
            // window.zoneType = document.createElement('select')
            window.zones.get(textareaMarker.id.substring(7)).zoneType.setAttribute('class', "form-select");
            window.zones.get(textareaMarker.id.substring(7)).zoneType.setAttribute('style', "width: 180px;");
            window.zones.get(textareaMarker.id.substring(7)).zoneType.setAttribute('id', "ZoneFigure-" + questionIndex);
            window.zones.get(textareaMarker.id.substring(7)).zoneType.setAttribute('name', "ZoneFigure-" + questionIndex);
            let circleVis = document.createElement('option')
            circleVis.setAttribute('class', "lang");
            circleVis.setAttribute('key', "circle");
            circleVis.textContent = "Окружность"
            let polygon = document.createElement('option')
            polygon.setAttribute('class', "lang");
            polygon.setAttribute('key', "polygon");
            polygon.textContent = "Многоугольник"
            let divCoords = document.createElement('div');
            divCoords.setAttribute('style', "width: 160px; margin-left: 8px; margin-right: 4px;");
            divCoords.setAttribute('key', "coordinates");
            divCoords.setAttribute('class', "lang");
            divCoords.textContent = "Координаты";
            // let window.zones.get(textareaMarker.id.substring(7)).textareaCoords = document.createElement('textarea');
            window.zones.get(textareaMarker.id.substring(7)).textareaCoords = document.createElement('textarea');
            window.zones.get(textareaMarker.id.substring(7)).textareaCoords.setAttribute('class', "form-control langp");
            window.zones.get(textareaMarker.id.substring(7)).textareaCoords.setAttribute('key', "zone_coordinates");
            window.zones.get(textareaMarker.id.substring(7)).textareaCoords.setAttribute('placeholder', "Координаты зоны");
            window.zones.get(textareaMarker.id.substring(7)).textareaCoords.setAttribute('name', "Coordinates-" + questionIndex + "-" + answerIndex);
            window.zones.get(textareaMarker.id.substring(7)).textareaCoords.setAttribute('id', "Coordinates-" + questionIndex + "-" + answerIndex);
            window.zones.get(textareaMarker.id.substring(7)).textareaCoords.setAttribute('rows', "1");
            window.zones.get(textareaMarker.id.substring(7)).textareaCoords.setAttribute('maxlength', '5000');

            let buttonDel = document.createElement('button');
            buttonDel.setAttribute('class', "btn");
            buttonDel.setAttribute('style', "background-color:red; color:white; padding: 4px; width: 25px;");
            buttonDel.setAttribute('onclick', "deleteElement(\"delAns-\" + this.id); window.zones.delete(this.name + \"-\" + this.id); window.draw_figures();");
            buttonDel.textContent = "✖"
            buttonDel.setAttribute('id', answerIndex);
            buttonDel.setAttribute('name', questionIndex);
            let divDel = document.createElement('div');
            divDel.setAttribute('style', "padding-left: 5px;");

            addDragoverEventListener(divIndexNew, `answer_div`);
            let divAnsCard = addDragndropDesign(divTextLabel, 'answer');

            let markNote = document.createElement('div');
            markNote.setAttribute('style', "color: gray; font-size: 14px;");
            markNote.setAttribute('class', "to_del lang");
            markNote.setAttribute('key', "markNote");
            markNote.setAttribute('key', "markNote");
            markNote.textContent = "*Примечание: в координатах зоны последовательно указаны координаты x, y каждой вершины многоуголинка, или же координаты центра и радиус для окружности";

            span.appendChild(divFlex)
            divFlex.appendChild(divCanv)
            divCanv.appendChild(canvas)
            divFlex.appendChild(form)
            form.appendChild(inputFile)
            form.appendChild(aForButton)
            aForButton.appendChild(aButton)
            divIndexNew.appendChild(divTextLabel)
            divTextLabel.appendChild(divMarker)
            divTextLabel.appendChild(textareaMarker)
            divTextLabel.appendChild(divZone)
            divTextLabel.appendChild(window.zones.get(textareaMarker.id.substring(7)).zoneType)
            window.zones.get(textareaMarker.id.substring(7)).zoneType.appendChild(polygon)
            window.zones.get(textareaMarker.id.substring(7)).zoneType.appendChild(circleVis)
            divTextLabel.appendChild(divCoords)
            divTextLabel.appendChild(window.zones.get(textareaMarker.id.substring(7)).textareaCoords)
            divDel.appendChild(buttonDel)
            divTextLabel.appendChild(divDel)
            divTextLabel.appendChild(divAnsCard)
            let divIndexTmp = document.getElementById("addAns-" + questionIndexButtonId)
            divIndexTmp.replaceWith(divIndexNew);
            divIndexNew.parentElement.insertBefore(span, divIndexNew)
            divIndexNew.parentElement.insertBefore(markNote, divIndexNew.nextElementSibling)
            divIndexNew.parentElement.insertBefore(div_shuffle, markNote)
            let buttonNew = document.getElementById(questionIndexButtonId)
            buttonNew.removeAttribute("disabled");

            window.ctx=canvas.getContext("2d");
            var BB=canvas.getBoundingClientRect();
            window.scrollOffsetY = document.getElementsByClassName("content")[0].scrollTop;
            window.offsetX=BB.left;
            window.offsetY=BB.top;
            window.WIDTH = canvas.width;
            window.HEIGHT = canvas.height;
            window.vertexRadius = 6
            window.zones.get(textareaMarker.id.substring(7)).marker_name = "";

            // listen for mouse events
            canvas.onmousedown = myDown;
            canvas.onmouseup = myUp;
            canvas.onmousemove = myMove;

            // call to draw the scene
            draw_figures();

            textareaMarker.addEventListener('input', function (evt) {
                window.zones.get(textareaMarker.id.substring(7)).marker_name = textareaMarker.value;
                draw_figures();
            });

            window.zones.get(textareaMarker.id.substring(7)).zoneType.addEventListener('change', function (evt) {
                selectedOption = window.zones.get(textareaMarker.id.substring(7)).zoneType.options[window.zones.get(textareaMarker.id.substring(7)).zoneType.selectedIndex];
                if(selectedOption.getAttribute('key') === "polygon") {
                    window.zones.set(textareaMarker.id.substring(7), {vertexes:[{x:10,y:10,v:false},{x:10,y:60,v:false},{x:60,y:60,v:false},{x:60,y:10,v:false}],isDragging:false,selected:false,zoneType:window.zones.get(textareaMarker.id.substring(7)).zoneType, marker_name:textareaMarker.value, textareaCoords:window.zones.get(textareaMarker.id.substring(7)).textareaCoords});
                }else if(selectedOption.getAttribute('key') === "circle") {
                    window.zones.set(textareaMarker.id.substring(7), {x:60,y:60,radius:40,isDragging:false,selected:false,zoneType:window.zones.get(textareaMarker.id.substring(7)).zoneType, marker_name:textareaMarker.value, textareaCoords:window.zones.get(textareaMarker.id.substring(7)).textareaCoords});
                }
                draw_figures();
            });

            aButton.addEventListener('click', function (evt) {
                let file = inputFile.files[0];
                let reader = new FileReader();
                reader.onload = function(event) {
                    const image = new Image();
                    image.src = event.target.result;
                    image.onload = function () {
                        let height = this.height;
                        let width = this.width;
                        if(width > 1036){
                            let ratio = height / width;
                            width = 1036;
                            height = width * ratio;
                            ImageTools.resize(file, {
                                width: width,
                                height: height
                            }, function(blob, didItResize) {
                                canvas.height = height;
                                canvas.width = width;
                                divCanv.setAttribute("height", height + "px");
                                divCanv.setAttribute("width", width + "px");
                                $("#canvas-" + questionIndexButtonId).css('background-image', 'url(' + window.URL.createObjectURL(blob) + ')');
                                draw_figures();
                            });
                        }else{
                            canvas.height = height;
                            canvas.width = width;
                            divCanv.setAttribute("height", height + "px");
                            divCanv.setAttribute("width", width + "px");
                            $("#canvas-" + questionIndexButtonId).css('background-image', 'url(' + image.src + ')');
                            draw_figures();
                        }
                    };
                };
                reader.readAsDataURL(file);
            });

            window.zones.get(textareaMarker.id.substring(7)).textareaCoords.addEventListener('input', function (evt) {
                let string = window.zones.get(textareaMarker.id.substring(7)).textareaCoords.value;

                selectedOption = window.zones.get(textareaMarker.id.substring(7)).zoneType.options[window.zones.get(textareaMarker.id.substring(7)).zoneType.selectedIndex];
                if(selectedOption.getAttribute('key') === "polygon") {
                    let coordsAmount = window.zones.get(textareaMarker.id.substring(7)).textareaCoords.value.match(/;/g).length;
                    let delimiter, coords, comma;
                    window.zones.get(window.zones.get(textareaMarker.id.substring(7)).textareaCoords.id.substring(12)).vertexes = []
                    for(let i = 0; i < coordsAmount; i++){
                        if(i > 0){
                            delimiter = string.indexOf(";");
                            string = string.slice(delimiter+1);
                        }
                        delimiter = string.indexOf(";");
                        if(delimiter > 0)
                            coords = string.slice(0, delimiter);
                        else
                            coords = string
                        comma = coords.indexOf(",");
                        let new_x = parseInt(coords.slice(0, comma));
                        let new_y = parseInt(coords.slice(comma+1));
                        window.zones.get(window.zones.get(textareaMarker.id.substring(7)).textareaCoords.id.substring(12)).vertexes.push({x:new_x, y: new_y, v:false})
                    }
                } else if(selectedOption.getAttribute('key') === "circle") {
                    let circle = window.zones.get(window.zones.get(textareaMarker.id.substring(7)).textareaCoords.id.substring(12));
                    let delimiter = string.indexOf(",");
                    circle.x = parseInt(string.slice(0, delimiter));
                    string = string.slice(delimiter+1);
                    delimiter = string.indexOf(",");
                    circle.y = parseInt(string.slice(0, delimiter));
                    string = string.slice(delimiter+1);
                    circle.radius = parseInt(string);
                }
                draw_figures(false);
            });
        }
        if (selectedOption.getAttribute('key') === "detailed_free" || selectedOption.getAttribute('key') === "free") {
            textareaQuestion.setAttribute('rows', "1");
            let divIndexNew = document.createElement('div');
            divIndexNew.setAttribute('class', "row container-fluid");
            divIndexNew.setAttribute('id', "addAns-" + questionIndexButtonId);
            let divTextLabel = document.createElement('div');
            divTextLabel.setAttribute('style', "padding-bottom: 10px; display: flex; align-items: center;");
            divTextLabel.setAttribute('id', "delAns-" + answerIndex);
            let textareaAnswer = document.createElement('textarea');
            textareaAnswer.setAttribute('class', "form-control");
            textareaAnswer.setAttribute('name', "Answer-" + questionIndex + "-" + answerIndex);
            if (selectedOption.getAttribute('key') === "free") {
                textareaAnswer.setAttribute('placeholder', "Краткий ответ");
                if(textareaAnswer.className.indexOf(" langp") < 0)
                    textareaAnswer.setAttribute('class', textareaAnswer.className + " langp");
                textareaAnswer.setAttribute('key', "short_answer");
                textareaAnswer.setAttribute('rows', "1");
                textareaAnswer.removeAttribute("disabled");
                textareaAnswer.setAttribute('maxlength', '5000');
            }
            if (selectedOption.getAttribute('key') === "detailed_free") {
                textareaAnswer.setAttribute('placeholder', "Развернутый ответ");
                if(textareaAnswer.className.indexOf(" langp") < 0)
                    textareaAnswer.setAttribute('class', textareaAnswer.className + " langp");
                textareaAnswer.setAttribute('key', "long_answer");
                textareaAnswer.setAttribute('rows', "8");
                textareaAnswer.setAttribute("disabled", "true");
                textareaAnswer.setAttribute('maxlength', '15000');
            }
            divIndexNew.appendChild(divTextLabel)
            divTextLabel.appendChild(textareaAnswer)
            let divIndexTmp = document.getElementById("addAns-" + questionIndexButtonId)
            divIndexTmp.replaceWith(divIndexNew);
            let buttonNew = document.getElementById(questionIndexButtonId)
            buttonNew.setAttribute("disabled", "true");
        }
        if (selectedOption.getAttribute('key') === "info_block") {
            textareaQuestion.setAttribute('placeholder', "Информация");
            textareaQuestion.setAttribute('rows', "8");
            if(textareaQuestion.className.indexOf(" langp") < 0)
                textareaQuestion.setAttribute('class', textareaQuestion.className + " langp");
            textareaQuestion.setAttribute('key', "information");
            let divIndexNew = document.createElement('div');
            divIndexNew.setAttribute('class', "row container-fluid");
            divIndexNew.setAttribute('id', "addAns-" + questionIndexButtonId);
            let divIndexTmp = document.getElementById("addAns-" + questionIndexButtonId)
            divIndexTmp.replaceWith(divIndexNew);
            let buttonNew = document.getElementById(questionIndexButtonId)
            buttonNew.setAttribute("disabled", "true");
        } else {
            textareaQuestion.setAttribute('placeholder', "Текст вопроса");
            if(textareaQuestion.className.indexOf(" langp") < 0)
                textareaQuestion.setAttribute('class', extareaQuestion.className + " langp");
            textareaQuestion.setAttribute('key', "question_text");
        }

        answerIndex += 1;

        let lang = localStorage.getItem('language');
        translate(lang);
    });
}

export function translate(lang) {
    $('.lang').each(function (index, item) {
        $(this).text(arrLang[lang][$(this).attr('key')]);
        $('.curflag').removeClass('flag-united-kingdom').removeClass('flag-russia').removeClass('flag-germany').removeClass('flag-france').removeClass('flag-spain').removeClass('flag-portugal').removeClass('flag-china').removeClass('flag-japan').addClass(arrLang[lang][$('.curflag').attr('key')]);
    });
    $('.langp').each(function (index, item) {
        $(this).attr("placeholder", arrLang[lang][$(this).attr('key')]);
    });
}

export function change_language(lang) {
    document.querySelectorAll(".tick").forEach(elem =>{
        elem.style.visibility = "hidden";
    });
    if (lang === "en") {
        document.getElementById("en-tick").style.visibility = "visible";
        localStorage.setItem('language', 'en')
    } else if (lang === "ru") {
        document.getElementById("ru-tick").style.visibility = "visible";
        localStorage.setItem('language', 'ru')
    } else if (lang === "de") {
        document.getElementById("de-tick").style.visibility = "visible";
        localStorage.setItem('language', 'de')
    } else if (lang === "fr") {
        document.getElementById("fr-tick").style.visibility = "visible";
        localStorage.setItem('language', 'fr')
    } else if (lang === "es") {
        document.getElementById("es-tick").style.visibility = "visible";
        localStorage.setItem('language', 'es')
    } else if (lang === "pt") {
        document.getElementById("pt-tick").style.visibility = "visible";
        localStorage.setItem('language', 'pt')
    } else if (lang === "cn") {
        document.getElementById("cn-tick").style.visibility = "visible";
        localStorage.setItem('language', 'cn')
    } else if (lang === "jp") {
        document.getElementById("jp-tick").style.visibility = "visible";
        localStorage.setItem('language', 'jp')
    }
    translate(lang);
}
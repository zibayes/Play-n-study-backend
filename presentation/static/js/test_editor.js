let dnd_elems = []
let card_elems = []
let questionsTypes = []
let addAns_elems = []
for(i = 1; i <= questions_count; i++){
    dnd_elems.push(document.getElementById("dnd-" + i))
    card_elems.push(document.getElementById("card-" + i))

    dnd_elems[i-1].addEventListener(`mouseover`, (evt) => {
      document.body.style.cursor = 'move';
    })
    dnd_elems[i-1].addEventListener(`mouseout`, (evt) => {
      document.body.style.cursor = '';
    })
    dnd_elems[i-1].addEventListener(`dragstart`, (evt) => {
      evt.dataTransfer.setDragImage(card_elems[parseInt(evt.target.className) - 1], card_elems[parseInt(evt.target.className) - 1].offsetWidth / 1.78, card_elems[parseInt(evt.target.className) - 1].offsetHeight / 18)
      setTimeout(() => {
          card_elems[parseInt(evt.target.className) - 1].classList.add(`selected`);
          card_elems[parseInt(evt.target.className) - 1].style.visibility  = "hidden"
      }, 0);
    })
    dnd_elems[i-1].addEventListener(`dragend`, (evt) => {
      setTimeout(() => {
          card_elems[parseInt(evt.target.className) - 1].classList.remove(`selected`);
          card_elems[parseInt(evt.target.className) - 1].style.removeProperty("visibility")
      }, 0);
    });

    questionsTypes.push(document.getElementById("QT-" + i))
    questionsTypes[i-1].addEventListener("change", function() {
    let selectedOption = questionsTypes[parseInt(this.id.slice(3))-1].options[questionsTypes[parseInt(this.id.slice(3))-1].selectedIndex];
        let textareaQuestion = document.getElementById("ask-" + (parseInt(this.name.slice(13))))
        if(selectedOption.text === "Единственный ответ" ||  selectedOption.text === "Множественный ответ") {
            textareaQuestion.setAttribute('rows', "1");
            let divIndexNew = document.createElement('div');
            divIndexNew.setAttribute('class', "row container-fluid");
            divIndexNew.setAttribute('id', "addAns-" + parseInt(this.name.slice(13)));
            let divTextLabel = document.createElement('div');
            divTextLabel.setAttribute('style', "padding-bottom: 10px; display: flex; align-items: center;");
            divTextLabel.setAttribute('id', "delAns-" + answerIndex);
            divTextLabel.setAttribute('class', "answer_div");
            let textareaAnswer = document.createElement('textarea');
            textareaAnswer.setAttribute('class', "form-control");
            textareaAnswer.setAttribute('maxlength', '5000');
            textareaAnswer.setAttribute('placeholder', "Текст ответа");
            textareaAnswer.setAttribute('name', "Answer-" + questionIndex + "-" + answerIndex);
            textareaAnswer.setAttribute('rows', "1");
            let label = document.createElement('label');
            label.setAttribute('for', "addAnswerText");
            label.setAttribute('style', "padding-right: 8px;");
            let input = document.createElement('input');
            //input.setAttribute('required', 'true');
            if (selectedOption.text === "Единственный ответ") {
                input.setAttribute('type', "radio");
                input.setAttribute('name', "Right_Answer-" + parseInt(this.name.slice(13)));
            }
            if (selectedOption.text === "Множественный ответ") {
                input.setAttribute('type', "checkbox");
                input.setAttribute('name', "Right_Answer-" + parseInt(this.name.slice(13)) + "-" + answerIndex);
            }
            let buttonDel = document.createElement('button');
            buttonDel.setAttribute('class', "btn");
            buttonDel.setAttribute('style', "background-color:red; color:white; padding: 4px; width: 25px;");
            buttonDel.setAttribute('onclick', "deleteElement(\"delAns-\" + this.id)");
            buttonDel.textContent = "✖"
            buttonDel.setAttribute('id', answerIndex);
            let divDel = document.createElement('div');
            divDel.setAttribute('style', "padding-left: 5px;");

            var isAbleToMove = true;
            divIndexNew.addEventListener(`dragover`, (evt) => {
                evt.preventDefault();
                const activeElement = questions_list.querySelector(`.selected`);
                const currentElement = evt.target;
                const isMoveable = activeElement !== currentElement && isAbleToMove &&
                currentElement.classList.contains(`answer_div`) && activeElement.classList.contains(`answer_div`) && childOf(activeElement, divIndexNew);
                if (!isMoveable)
                    return;
                isAbleToMove = false;
                let nextElement;
                if(currentElement === activeElement.nextElementSibling){
                    nextElement = currentElement.nextElementSibling;
                    currentElement.animate(
                      [
                        // keyframes
                        { transform: "translateY(" + activeElement.offsetHeight + "px)" },
                        { transform: "translateY(" + 0 + "px)" },
                      ],
                      {
                        // timing options
                        duration: 300,
                        iterations: 1,
                      }
                    );
                } else {
                    nextElement = currentElement;
                    currentElement.animate(
                      [
                        // keyframes
                        { transform: "translateY(-" + activeElement.offsetHeight + "px)" },
                        { transform: "translateY(" + 0 + "px)" },
                      ],
                      {
                        // timing options
                        duration: 300,
                        iterations: 1,
                      }
                    );
                }
                divIndexNew.insertBefore(activeElement, nextElement);
                setTimeout(() => {isAbleToMove = true;}, 400)
            });
            let divAnsCard = document.createElement('div');
            divAnsCard.setAttribute('style', "height: 30px; justify-content: center; display: flex;");
            let dragAnsImg = document.createElement('img');
            dragAnsImg.setAttribute('src', "/static/img/drag_n_drop.png");
            dragAnsImg.setAttribute('style', "height: 30px; transform: rotate(90deg);");
            divAnsCard.setAttribute('draggable', "True");
            divAnsCard.addEventListener(`mouseover`, (evt) => {
              document.body.style.cursor = 'move';
            })
            divAnsCard.addEventListener(`mouseout`, (evt) => {
              document.body.style.cursor = '';
            })
            divAnsCard.addEventListener(`dragstart`, (evt) => {
              evt.dataTransfer.setDragImage(divTextLabel, divTextLabel.offsetWidth / 1.032, divTextLabel.offsetHeight / 2)
              setTimeout(() => {
                  divTextLabel.classList.add(`selected`);
                  divTextLabel.style.visibility  = "hidden"
              }, 0);
            })
            divAnsCard.addEventListener(`dragend`, (evt) => {
              setTimeout(() => {
                  divTextLabel.classList.remove(`selected`);
                  divTextLabel.style.removeProperty("visibility")
              }, 0);
            });

            divIndexNew.appendChild(divTextLabel)
            label.appendChild(input)
            divTextLabel.appendChild(label)
            divTextLabel.appendChild(textareaAnswer)
            divDel.appendChild(buttonDel)
            divTextLabel.appendChild(divDel)
            divTextLabel.appendChild(divAnsCard)
            divAnsCard.appendChild(dragAnsImg)
            let divIndexTmp = document.getElementById("addAns-" + parseInt(this.name.slice(13)))
            divIndexTmp.replaceWith(divIndexNew);
            let buttonNew = document.getElementById(parseInt(this.name.slice(13)))
            buttonNew.removeAttribute("disabled");
        }
        if(selectedOption.text === "Свободный ответ" || selectedOption.text === "Краткий свободный ответ") {
            textareaQuestion.setAttribute('rows', "1");
            let divIndexNew = document.createElement('div');
            divIndexNew.setAttribute('class', "row container-fluid");
            divIndexNew.setAttribute('id', "addAns-" + parseInt(this.name.slice(13)));
            let divTextLabel = document.createElement('div');
            divTextLabel.setAttribute('style', "padding-bottom: 10px; display: flex; align-items: center;");
            divTextLabel.setAttribute('id', "delAns-" + answerIndex);
            let textareaAnswer = document.createElement('textarea');
            textareaAnswer.setAttribute('class', "form-control");
            textareaAnswer.setAttribute('name', "Answer-" + questionIndex + "-" + answerIndex);
            if (selectedOption.text === "Краткий свободный ответ") {
                textareaAnswer.setAttribute('placeholder', "Краткий ответ");
                textareaAnswer.setAttribute('rows', "1");
                textareaAnswer.removeAttribute("disabled");
                textareaAnswer.setAttribute('maxlength', '5000');
            }
            if (selectedOption.text === "Свободный ответ") {
                textareaAnswer.setAttribute('placeholder', "Развернутый ответ");
                textareaAnswer.setAttribute('rows', "8");
                textareaAnswer.setAttribute("disabled", "true");
                textareaAnswer.setAttribute('maxlength', '15000');
            }
            divIndexNew.appendChild(divTextLabel)
            divTextLabel.appendChild(textareaAnswer)
            let divIndexTmp = document.getElementById("addAns-" + parseInt(this.name.slice(13)))
            divIndexTmp.replaceWith(divIndexNew);
            let buttonNew = document.getElementById(parseInt(this.name.slice(13)))
            buttonNew.setAttribute("disabled", "true");
        }
        if(selectedOption.text === "Информационный блок"){
            textareaQuestion.setAttribute('placeholder', "Информация");
            textareaQuestion.setAttribute('rows', "8");
            let divIndexNew = document.createElement('div');
            divIndexNew.setAttribute('class', "row container-fluid");
            divIndexNew.setAttribute('id', "addAns-" + parseInt(this.name.slice(13)));
            let divIndexTmp = document.getElementById("addAns-" + parseInt(this.name.slice(13)))
            divIndexTmp.replaceWith(divIndexNew);
            let buttonNew = document.getElementById(parseInt(this.name.slice(13)))
            buttonNew.setAttribute("disabled", "true");
        } else {
            textareaQuestion.setAttribute('placeholder', "Текст вопроса");
        }
        answerIndex += 1;
    });

    addAns_elems.push(document.getElementById("addAns-" + i))
    var isAbleToMoveAdd = true;
    addAns_elems[i-1].addEventListener(`dragover`, (evt) => {
        evt.preventDefault();
        const activeElement = questions_list.querySelector(`.selected`);
        const currentElement = evt.target.parentElement.parentElement;
        const isMoveable = activeElement !== currentElement && isAbleToMoveAdd &&
        currentElement.classList.contains(`answer_div`) && activeElement.classList.contains(`answer_div`) && childOf(activeElement, addAns_elems[parseInt(evt.target.id)-1]);
        if (!isMoveable)
            return;
        isAbleToMoveAdd = false;
        let nextElement;
        if(currentElement === activeElement.nextElementSibling){
            nextElement = currentElement.nextElementSibling;
            currentElement.animate(
              [
                // keyframes
                { transform: "translateY(" + activeElement.offsetHeight + "px)" },
                { transform: "translateY(" + 0 + "px)" },
              ],
              {
                // timing options
                duration: 200,
                iterations: 1,
              }
            );
        } else {
            nextElement = currentElement;
            currentElement.animate(
              [
                // keyframes
                { transform: "translateY(-" + activeElement.offsetHeight + "px)" },
                { transform: "translateY(" + 0 + "px)" },
              ],
              {
                // timing options
                duration: 300,
                iterations: 1,
              }
            );
        }
        addAns_elems[parseInt(evt.target.id)-1].insertBefore(activeElement, nextElement);
        setTimeout(() => {isAbleToMoveAdd = true;}, 400)
    });
}
document.querySelectorAll(".dnd").forEach(elem =>{
    elem.addEventListener(`mouseover`, (evt) => {
      document.body.style.cursor = 'move';
    })
    elem.addEventListener(`mouseout`, (evt) => {
      document.body.style.cursor = '';
    })
    let divTextLabel = document.getElementById("Answer-" + elem.id);
    elem.addEventListener(`dragstart`, (evt) => {
      evt.dataTransfer.setDragImage(divTextLabel, divTextLabel.offsetWidth / 1.032, divTextLabel.offsetHeight / 2)
      setTimeout(() => {
          divTextLabel.classList.add(`selected`);
          divTextLabel.style.visibility  = "hidden"
      }, 0);
    })
    elem.addEventListener(`dragend`, (evt) => {
      setTimeout(() => {
          divTextLabel.classList.remove(`selected`);
          divTextLabel.style.removeProperty("visibility")
      }, 0);
    });
});

function childOf(c,p){while((c=c.parentNode)&&c!==p);return !!c}
let questions_list = document.getElementById("questionsList")
var isAbleToMoveQue = true;
questions_list.addEventListener(`dragover`, (evt) => {
    evt.preventDefault();
    const activeElement = questions_list.querySelector(`.selected`);
    const currentElement = evt.target;
    const isMoveable = activeElement !== currentElement && isAbleToMoveQue &&
    currentElement.classList.contains(`question_div`) && activeElement.classList.contains(`question_div`);
    if (!isMoveable)
        return;
    isAbleToMoveQue = false;
    let nextElement;
    if(currentElement === activeElement.nextElementSibling){
        nextElement = currentElement.nextElementSibling;
        currentElement.animate(
          [
            // keyframes
            { transform: "translateY(" + activeElement.offsetHeight + "px)" },
            { transform: "translateY(" + 0 + "px)" },
          ],
          {
            // timing options
            duration: 300,
            iterations: 1,
          }
        );
    } else {
        nextElement = currentElement;
        currentElement.animate(
          [
            // keyframes
            { transform: "translateY(-" + activeElement.offsetHeight + "px)" },
            { transform: "translateY(" + 0 + "px)" },
          ],
          {
            // timing options
            duration: 300,
            iterations: 1,
          }
        );
    }
    questions_list.insertBefore(activeElement, nextElement);
    setTimeout(() => {isAbleToMoveQue = true;}, 400)
});

// Добавление вопроса
let addBtn = document.getElementById("addQuestion");
var questionIndex = questions_count;
var answerIndex = 0;
addBtn.addEventListener("click", function(e) {
    // Внешний div
    let div = document.createElement('div');
    div.setAttribute('id', "delQue-" + questionIndex);
    div.setAttribute('class', "question_div");
    // Карточка вопроса
    let divCard = document.createElement('div');
    divCard.setAttribute('class', "card");

    // Drag'n'drop область
    let divDragCard = document.createElement('div');
    divDragCard.setAttribute('style', "height: 35px; justify-content: center; display: flex;");
    let dragImg = document.createElement('img');
    dragImg.setAttribute('src', "/static/img/drag_n_drop.png");
    dragImg.setAttribute('style', "height: 35px;");
    divDragCard.setAttribute('draggable', "True");
    divDragCard.addEventListener(`mouseover`, (evt) => {
      document.body.style.cursor = 'move';
    })
    divDragCard.addEventListener(`mouseout`, (evt) => {
      document.body.style.cursor = '';
    })
    divDragCard.addEventListener(`dragstart`, (evt) => {
      evt.dataTransfer.setDragImage(div, div.offsetWidth / 1.78, div.offsetHeight / 18)
      setTimeout(() => {
          div.classList.add(`selected`);
          div.style.visibility  = "hidden"
      }, 0);
    })
    divDragCard.addEventListener(`dragend`, (evt) => {
      setTimeout(() => {
          div.classList.remove(`selected`);
          div.style.removeProperty("visibility")
      }, 0);
    });

    let divCardBody = document.createElement('div');
    divCardBody.setAttribute('class', "card-body");
    let formGroup = document.createElement('div');
    formGroup.setAttribute('class', "form-group");
    // Содержимое карточки
    let textareaQuestion = document.createElement('textarea');
    textareaQuestion.setAttribute('class', "form-control");
    textareaQuestion.setAttribute('placeholder', "Текст вопроса");
    textareaQuestion.setAttribute('id', "question");
    textareaQuestion.setAttribute('maxlength', '5000');
    textareaQuestion.setAttribute('rows', "1");
    textareaQuestion.setAttribute('required', 'true');
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
    textareaAnswer.setAttribute('class', "form-control");
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
    button.setAttribute('class', "btn");
    button.setAttribute('style', "background-color:transparent; color:black;");
    button.setAttribute('onclick', "addAnswerOnButtonClick(\"addAns-\" + this.id)");
    button.textContent = "Добавить ответ"
    button.setAttribute('id', questionIndex);
    button.setAttribute('type', "button");
    input.setAttribute('name', "Right_Answer-" +  answerIndex);
    let buttonDelQuestion = document.createElement('button');
    buttonDelQuestion.setAttribute('class', "btn");
    buttonDelQuestion.setAttribute('type', "button");
    buttonDelQuestion.setAttribute('style', "background-color:red; color:white;");
    buttonDelQuestion.setAttribute('onclick', "deleteElement(\"delQue-\" + this.id)");
    buttonDelQuestion.textContent = "Удалить вопрос"
    buttonDelQuestion.setAttribute('id', questionIndex);
    let buttonUpQuestion = document.createElement('button');
    buttonUpQuestion.setAttribute('type', "button");
    buttonUpQuestion.setAttribute('class', "btn");
    buttonUpQuestion.setAttribute('style', "background-color:white; color:black; padding: 4px; width: 35px; height: 35px; font-size:20px;");
    buttonUpQuestion.addEventListener("click", function() {
        let questionsList = document.getElementById("questionsList");
        questionsList.insertBefore(div, div.previousElementSibling);
    });
    buttonUpQuestion.textContent = "↑"
    let buttonDownQuestion = document.createElement('button');
    buttonDownQuestion.setAttribute('type', "button");
    buttonDownQuestion.setAttribute('class', "btn");
    buttonDownQuestion.setAttribute('style', "background-color:white; color:black; padding: 4px; width: 35px; height: 35px; font-size:20px;");
    buttonDownQuestion.addEventListener("click", function() {
        let questionsList = document.getElementById("questionsList");
        if(div.nextElementSibling == null){
            questionsList.insertBefore(div, questionsList.firstChild);
        }else{
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

    var isAbleToMoveDivInd = true;
    divIndex.addEventListener(`dragover`, (evt) => {
        evt.preventDefault();
        const activeElement = questions_list.querySelector(`.selected`);
        const currentElement = evt.target;
        const isMoveable = activeElement !== currentElement && isAbleToMoveDivInd &&
        currentElement.classList.contains(`answer_div`) && activeElement.classList.contains(`answer_div`) && childOf(activeElement, divIndex);
        if (!isMoveable)
            return;
        isAbleToMoveDivInd = false;
        let nextElement;
        if(currentElement === activeElement.nextElementSibling){
            nextElement = currentElement.nextElementSibling;
            currentElement.animate(
              [
                // keyframes
                { transform: "translateY(" + activeElement.offsetHeight + "px)" },
                { transform: "translateY(" + 0 + "px)" },
              ],
              {
                // timing options
                duration: 300,
                iterations: 1,
              }
            );
        } else {
            nextElement = currentElement;
            currentElement.animate(
              [
                // keyframes
                { transform: "translateY(-" + activeElement.offsetHeight + "px)" },
                { transform: "translateY(" + 0 + "px)" },
              ],
              {
                // timing options
                duration: 300,
                iterations: 1,
              }
            );
        }
        divIndex.insertBefore(activeElement, nextElement);
        setTimeout(() => {isAbleToMoveDivInd = true;}, 400)
    });
    let divAnsCard = document.createElement('div');
    divAnsCard.setAttribute('style', "height: 30px; justify-content: center; display: flex;");
    let dragAnsImg = document.createElement('img');
    dragAnsImg.setAttribute('src', "/static/img/drag_n_drop.png");
    dragAnsImg.setAttribute('style', "height: 30px; transform: rotate(90deg);");
    divAnsCard.setAttribute('draggable', "True");
    divAnsCard.addEventListener(`mouseover`, (evt) => {
      document.body.style.cursor = 'move';
    })
    divAnsCard.addEventListener(`mouseout`, (evt) => {
      document.body.style.cursor = '';
    })
    divAnsCard.addEventListener(`dragstart`, (evt) => {
      evt.dataTransfer.setDragImage(divTextLabel, divTextLabel.offsetWidth / 1.032, divTextLabel.offsetHeight / 2)
      setTimeout(() => {
          divTextLabel.classList.add(`selected`);
          divTextLabel.style.visibility  = "hidden"
      }, 0);
    })
    divAnsCard.addEventListener(`dragend`, (evt) => {
      setTimeout(() => {
          divTextLabel.classList.remove(`selected`);
          divTextLabel.style.removeProperty("visibility")
      }, 0);
    });

    let questionType = document.createElement('select')
    questionType.setAttribute('class', "form-select");
    questionType.setAttribute('width', "20px");
    questionType.setAttribute('id', "QT-" + questionIndex);
    questionType.setAttribute('name', "QuestionType-" + questionIndex);
    let radio = document.createElement('option')
    radio.textContent = "Единственный ответ"
    let check = document.createElement('option')
    check.textContent = "Множественный ответ"
    let word = document.createElement('option')
    word.textContent = "Краткий свободный ответ"
    let text = document.createElement('option')
    text.textContent = "Свободный ответ"
    let info = document.createElement('option')
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
    questionType.appendChild(word)
    questionType.appendChild(text)
    questionType.appendChild(info)
    questionType.addEventListener("change", function() {
    let selectedOption = questionType.options[questionType.selectedIndex];
        if(selectedOption.text === "Единственный ответ" ||  selectedOption.text === "Множественный ответ") {
            textareaQuestion.setAttribute('rows', "1");
            let divIndexNew = document.createElement('div');
            divIndexNew.setAttribute('class', "row container-fluid");
            divIndexNew.setAttribute('id', divIndex.id);
            let divTextLabel = document.createElement('div');
            divTextLabel.setAttribute('style', "padding-bottom: 10px; display: flex; align-items: center;");
            divTextLabel.setAttribute('id', "delAns-" + answerIndex);
            divTextLabel.setAttribute('class', "answer_div");
            let textareaAnswer = document.createElement('textarea');
            textareaAnswer.setAttribute('class', "form-control");
            textareaAnswer.setAttribute('placeholder', "Текст ответа");
            textareaAnswer.setAttribute('maxlength', '5000');
            textareaAnswer.setAttribute('name', "Answer-" + questionIndex + "-" + answerIndex);
            textareaAnswer.setAttribute('rows', "1");
            let label = document.createElement('label');
            label.setAttribute('for', "addAnswerText");
            label.setAttribute('style', "padding-right: 8px;");
            let input = document.createElement('input');
            //input.setAttribute('required', 'true');
            if (selectedOption.text === "Единственный ответ") {
                input.setAttribute('type', "radio");
                input.setAttribute('name', "Right_Answer-" + button.id);
            }
            if (selectedOption.text === "Множественный ответ") {
                input.setAttribute('type', "checkbox");
                input.setAttribute('name', "Right_Answer-" + button.id + "-" + answerIndex);
            }
            let buttonDel = document.createElement('button');
            buttonDel.setAttribute('class', "btn");
            buttonDel.setAttribute('style', "background-color:red; color:white; padding: 4px; width: 25px;");
            buttonDel.setAttribute('onclick', "deleteElement(\"delAns-\" + this.id)");
            buttonDel.textContent = "✖"
            buttonDel.setAttribute('id', answerIndex);
            let divDel = document.createElement('div');
            divDel.setAttribute('style', "padding-left: 5px;");

            var isAbleToMoveDivIndNew = true
            divIndexNew.addEventListener(`dragover`, (evt) => {
                evt.preventDefault();
                const activeElement = questions_list.querySelector(`.selected`);
                const currentElement = evt.target;
                const isMoveable = activeElement !== currentElement && isAbleToMoveDivIndNew &&
                currentElement.classList.contains(`answer_div`) && activeElement.classList.contains(`answer_div`) && childOf(activeElement, divIndexNew);
                if (!isMoveable)
                    return;
                isAbleToMoveDivIndNew = false;
                let nextElement;
                if(currentElement === activeElement.nextElementSibling){
                    nextElement = currentElement.nextElementSibling;
                    currentElement.animate(
                      [
                        // keyframes
                        { transform: "translateY(" + activeElement.offsetHeight + "px)" },
                        { transform: "translateY(" + 0 + "px)" },
                      ],
                      {
                        // timing options
                        duration: 300,
                        iterations: 1,
                      }
                    );
                } else {
                    nextElement = currentElement;
                    currentElement.animate(
                      [
                        // keyframes
                        { transform: "translateY(-" + activeElement.offsetHeight + "px)" },
                        { transform: "translateY(" + 0 + "px)" },
                      ],
                      {
                        // timing options
                        duration: 300,
                        iterations: 1,
                      }
                    );
                }
                divIndexNew.insertBefore(activeElement, nextElement);
                setTimeout(() => {isAbleToMoveDivIndNew = true;}, 400)
            });
            let divAnsCard = document.createElement('div');
            divAnsCard.setAttribute('style', "height: 30px; justify-content: center; display: flex;");
            let dragAnsImg = document.createElement('img');
            dragAnsImg.setAttribute('src', "/static/img/drag_n_drop.png");
            dragAnsImg.setAttribute('style', "height: 30px; transform: rotate(90deg);");
            divAnsCard.setAttribute('draggable', "True");
            divAnsCard.addEventListener(`mouseover`, (evt) => {
              document.body.style.cursor = 'move';
            })
            divAnsCard.addEventListener(`mouseout`, (evt) => {
              document.body.style.cursor = '';
            })
            divAnsCard.addEventListener(`dragstart`, (evt) => {
              evt.dataTransfer.setDragImage(divTextLabel, divTextLabel.offsetWidth / 1.032, divTextLabel.offsetHeight / 2)
              setTimeout(() => {
                  divTextLabel.classList.add(`selected`);
                  divTextLabel.style.visibility  = "hidden"
              }, 0);
            })
            divAnsCard.addEventListener(`dragend`, (evt) => {
              setTimeout(() => {
                  divTextLabel.classList.remove(`selected`);
                  divTextLabel.style.removeProperty("visibility")
              }, 0);
            });

            divIndexNew.appendChild(divTextLabel)
            label.appendChild(input)
            divTextLabel.appendChild(label)
            divTextLabel.appendChild(textareaAnswer)
            divDel.appendChild(buttonDel)
            divTextLabel.appendChild(divDel)
            divTextLabel.appendChild(divAnsCard)
            divAnsCard.appendChild(dragAnsImg)
            let divIndexTmp = document.getElementById(divIndex.id)
            divIndexTmp.replaceWith(divIndexNew);
            let buttonNew = document.getElementById(button.id)
            buttonNew.removeAttribute("disabled");
        }
        if(selectedOption.text === "Свободный ответ" || selectedOption.text === "Краткий свободный ответ") {
            textareaQuestion.setAttribute('rows', "1");
            let divIndexNew = document.createElement('div');
            divIndexNew.setAttribute('class', "row container-fluid");
            divIndexNew.setAttribute('id', divIndex.id);
            let divTextLabel = document.createElement('div');
            divTextLabel.setAttribute('style', "padding-bottom: 10px; display: flex; align-items: center;");
            divTextLabel.setAttribute('id', "delAns-" + answerIndex);
            let textareaAnswer = document.createElement('textarea');
            textareaAnswer.setAttribute('class', "form-control");
            textareaAnswer.setAttribute('name', "Answer-" + questionIndex + "-" + answerIndex);
            if (selectedOption.text === "Краткий свободный ответ") {
                textareaAnswer.setAttribute('placeholder', "Краткий ответ");
                textareaAnswer.setAttribute('rows', "1");
                textareaAnswer.removeAttribute("disabled");
                textareaAnswer.setAttribute('maxlength', '5000');
            }
            if (selectedOption.text === "Свободный ответ") {
                textareaAnswer.setAttribute('placeholder', "Развернутый ответ");
                textareaAnswer.setAttribute('rows', "8");
                textareaAnswer.setAttribute("disabled", "true");
                textareaAnswer.setAttribute('maxlength', '15000');
            }
            divIndexNew.appendChild(divTextLabel)
            divTextLabel.appendChild(textareaAnswer)
            let divIndexTmp = document.getElementById(divIndex.id)
            divIndexTmp.replaceWith(divIndexNew);
            let buttonNew = document.getElementById(button.id)
            buttonNew.setAttribute("disabled", "true");
        }
        if(selectedOption.text === "Информационный блок"){
            textareaQuestion.setAttribute('placeholder', "Информация");
            textareaQuestion.setAttribute('rows', "8");
            let divIndexNew = document.createElement('div');
            divIndexNew.setAttribute('class', "row container-fluid");
            divIndexNew.setAttribute('id', divIndex.id);
            let divIndexTmp = document.getElementById(divIndex.id)
            divIndexTmp.replaceWith(divIndexNew);
            let buttonNew = document.getElementById(button.id)
            buttonNew.setAttribute("disabled", "true");
        } else {
            textareaQuestion.setAttribute('placeholder', "Текст вопроса");
        }
        answerIndex += 1;
    });

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
    question.textContent = "Вопрос №" + (questionIndex + 1)
    let inputScore = document.createElement('input');
    inputScore.setAttribute('name', "score-" + questionIndex);
    inputScore.setAttribute('required', 'true');
    inputScore.setAttribute('style', 'width:40px;');
    inputScore.value = 1
    let labelScore = document.createElement('label');
    labelScore.setAttribute('for', "score-" + questionIndex);
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
    divDragCard.appendChild(dragImg)
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
    divAnsCard.appendChild(dragAnsImg)
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

    let answersElm = document.getElementById("questionsList");
    answersElm.appendChild(div)

    questionIndex += 1;
    answerIndex += 1;
});

// Добавление ответа на вопрос
function addAnswerOnButtonClick(index) {
    let div = document.createElement('div');
    div.setAttribute('style', "padding-bottom: 10px; display: flex; align-items: center;");
    div.setAttribute('id', "delAns-" + answerIndex);
    div.setAttribute('class', "answer_div");
    let textarea = document.createElement('textarea');
    textarea.setAttribute('class', "form-control");
    textarea.setAttribute('placeholder', "Текст ответа");
    textarea.setAttribute('maxlength', '5000');
    textarea.setAttribute('name', `Answer-${index.substring(7)}-${answerIndex}`);
    textarea.setAttribute('rows', "1");
    let label = document.createElement('label');
    label.setAttribute('for', "addAnswerText");
    label.setAttribute('style', "padding-right: 8px;");
    let input = document.createElement('input');
    //input.setAttribute('required', 'true');
    let questionType = document.getElementById(`QT-${index.substring(7)}`);
    let selectedOption = questionType.options[questionType.selectedIndex];
    if(selectedOption.text === "Единственный ответ") {
        input.setAttribute("type", "radio");
        input.setAttribute('name', `Right_Answer-${index.substring(7)}`);
    }
    if(selectedOption.text === "Множественный ответ") {
        input.setAttribute("type", "checkbox");
        input.setAttribute('name', `Right_Answer-${index.substring(7)}-${answerIndex}`);
    }
    let buttonDel = document.createElement('button');
    buttonDel.setAttribute('class', "btn");
    buttonDel.setAttribute('style', "background-color:red; color:white; padding: 4px; width: 25px;");
    buttonDel.setAttribute('onclick', "deleteElement(\"delAns-\" + this.id)");
    buttonDel.textContent = "✖"
    buttonDel.setAttribute('id', answerIndex);
    let divDel = document.createElement('div');
    divDel.setAttribute('style', "padding-left: 5px;");

    let divAnsCard = document.createElement('div');
    divAnsCard.setAttribute('style', "height: 30px; justify-content: center; display: flex;");
    let dragAnsImg = document.createElement('img');
    dragAnsImg.setAttribute('src', "/static/img/drag_n_drop.png");
    dragAnsImg.setAttribute('style', "height: 30px; transform: rotate(90deg);");
    divAnsCard.setAttribute('draggable', "True");
    divAnsCard.addEventListener(`mouseover`, (evt) => {
      document.body.style.cursor = 'move';
    })
    divAnsCard.addEventListener(`mouseout`, (evt) => {
      document.body.style.cursor = '';
    })
    divAnsCard.addEventListener(`dragstart`, (evt) => {
      evt.dataTransfer.setDragImage(div, div.offsetWidth / 1.032, div.offsetHeight / 2)
      setTimeout(() => {
          div.classList.add(`selected`);
          div.style.visibility  = "hidden"
      }, 0);
    })
    divAnsCard.addEventListener(`dragend`, (evt) => {
      setTimeout(() => {
          div.classList.remove(`selected`);
          div.style.removeProperty("visibility")
      }, 0);
    });

    label.appendChild(input)
    div.appendChild(label)
    div.appendChild(textarea)
    divDel.appendChild(buttonDel)
    div.appendChild(divDel)
    div.appendChild(divAnsCard)
    divAnsCard.appendChild(dragAnsImg)
    let answersElm = document.getElementById(index);
    answersElm.appendChild(div);

    answerIndex += 1;
}

// Удаление элемента
function deleteElement(index) {
    document.getElementById(index).remove()
}
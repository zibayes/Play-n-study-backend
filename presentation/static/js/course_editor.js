import {
    addDragoverEventListener,
    addDragndropDesignVoid,
    childOf
} from './test_constructor_functions.js';

function submitForm(){
     const inputs = document.querySelectorAll('.toSend');
     let inputs_to_send = {}
     inputs.forEach(elem =>{
         let testInputs = document.querySelectorAll('.toSend-' + elem.name.substring(elem.name.indexOf('-')+1));
         let testToSend = []
         testInputs.forEach(elem =>{
             testToSend.push(elem.classList[elem.classList.length-1])
         })
         inputs_to_send[elem.name] = Array(elem.value, testToSend)
     })
     console.log(inputs_to_send)
     const sending_form = document.getElementById("sendingForm");
     $.each(inputs_to_send, function(key, value){
         let textareaCourse = document.createElement('textarea');
         textareaCourse.setAttribute('class', "form-control");
         if (key === 'courseName') {
             textareaCourse.setAttribute('name', key);
             textareaCourse.setAttribute('hidden', 'hidden');
             textareaCourse.textContent = value[0];
             sending_form.appendChild(textareaCourse);
         }
         else{
             textareaCourse.setAttribute('name', key);
             textareaCourse.setAttribute('hidden', 'hidden');
             textareaCourse.textContent = value[0];
             sending_form.appendChild(textareaCourse);
             value[1].forEach(elem =>{
                 let textareaTest = document.createElement('textarea');
                 textareaTest.setAttribute('class', "form-control");
                 textareaTest.setAttribute('name', elem);
                 textareaTest.setAttribute('hidden', 'hidden');
                 textareaTest.textContent = elem;
                 sending_form.appendChild(textareaTest);
             })
         }
     });
     sending_form.submit();
}
document.querySelectorAll(".dnd").forEach(elem =>{
    let divUnitTest = document.getElementById("unit_test-" + elem.id);

    /*
    new Sortable(divUnitTest, {
        group: "shared",
        animation: 200,
        ghostClass: "blue-background-class"
    });
    */

    addDragndropDesignVoid(divUnitTest, elem, 'course')
});

var isAbleToMove = true;

document.querySelectorAll(".dnd-unit").forEach(elem => {
    let divUnitTests = document.getElementById("unit_tests-" + elem.id);
    divUnitTests.addEventListener(`dragover`, (evt) => {
        evt.preventDefault();
        let activeElement = divUnitTests.querySelector(`.selected`);
        let currentElement = evt.target;
        if (activeElement == null)
            return;
        let isMoveable = activeElement !== currentElement && isAbleToMove &&
            currentElement.classList.contains(`test_div`) && activeElement.classList.contains(`test_div`) && childOf(activeElement, divUnitTests);
        if (!isMoveable)
            return;
        isAbleToMove = false;
        let array_for_compare = Array.from(divUnitTests.children);
        console.log(array_for_compare.indexOf(currentElement), array_for_compare.indexOf(activeElement))
        if (array_for_compare.indexOf(currentElement) > array_for_compare.indexOf(activeElement)) {
            const nextElement = (currentElement === activeElement.nextElementSibling) ?
                activeElement.nextElementSibling :
                currentElement;
            nextElement.animate(
              [
                // keyframes
                { transform: "translateX(" + currentElement.offsetWidth + "px)" },
                { transform: "translateX(" + 0 + "px)" },
              ],
              {
                // timing options
                duration: 200,
                iterations: 1,
              }
            );
            divUnitTests.insertBefore(nextElement, activeElement);
        }
        else {
            const nextElement = (currentElement === activeElement.nextElementSibling) ?
                activeElement.nextElementSibling :
                currentElement;
            nextElement.animate(
              [
                // keyframes
                { transform: "translateX(-" + currentElement.offsetWidth + "px)" },
                { transform: "translateX(" + 0 + "px)" },
              ],
              {
                // timing options
                duration: 200,
                iterations: 1,
              }
            );
            divUnitTests.insertBefore(activeElement, nextElement);
        }
        setTimeout(() => {isAbleToMove = true;}, 400)
    });
});

document.querySelectorAll(".dnd-units").forEach(elem =>{
    let divUnit = document.getElementById("unit-" + elem.id);
    addDragndropDesignVoid(divUnit, elem, 'unit');
});

let units_list = document.getElementById("units_list");
addDragoverEventListener(units_list, `unit_div`);
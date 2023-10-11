import {
    change_language,
    translate
} from './test_constructor_functions.js';

let bg = document.querySelector('.mouse-parallax-bg');
window.addEventListener('mousemove', function(e) {
    let x = e.clientX / window.innerWidth;
    let y = e.clientY / window.innerHeight;
    bg.style.transform = 'translate(-' + x * 150 + 'px, -' + y * 150 + 'px)';
});

let div_main = document.getElementsByClassName('chats')[0]

setTimeout(() => {
$.ajax({
  url: '/get_chats',
  method: 'post',
  dataType: 'json',
  success: function(json_data){

    json_data.chats.sort(
            function (a, b){
              return new Date(b.time) - new Date(a.time)
            }
    )
    for (let i = 0; i < json_data.chats.length; i++){
      let div = add_element_chat(json_data.chats[i].chat_id, json_data.chats[i].time, json_data.chats[i].user_with, json_data.chats[i].from_who, json_data.chats[i].last_message, json_data.chats[i].checked, json_data.chats[i].user_with_id)
      div_main.appendChild(div)
    }
  },
  error: function(json_data){

  }
});
}, 400)


function add_element_chat(chat_id, time, user_with, from_who, last_message, checked, user_with_id) {
  // 1 +
  let div_add = document.createElement("div")
  div_add.setAttribute("class", "collapse mt-3")
  div_add.id = "collapse" + chat_id
  // 2 +
  let div_card = document.createElement("div")
  div_card.setAttribute("class", "card")
  // 3 +
  let button_exit = document.createElement("button")
  button_exit.setAttribute("class", "btn-close")
  button_exit.setAttribute("type", "button")
  button_exit.setAttribute("data-mdb-toggle", "collapse")
  let href = "#collapse" + chat_id
  button_exit.setAttribute("href", href)
  button_exit.style = "padding: 10px"
  // 4
  let div_card_body = document.createElement("div")
  div_card_body.setAttribute("class", "card-body")
  div_card_body.setAttribute("data-mdb-perfect-scrollbar", "true")
  div_card_body.style = "position: relative; height: 400px; overflow: auto;"
  div_card_body.id = "div" + chat_id
  // 5
  // Элементы чата тут будут
    let date_message
    $.ajax({
        url: '/get_dialog',
        method: 'post',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({"chat_id": chat_id}),
        success: function (data) {
          date_message = data.messages[data.messages.length - 1].msg_date
          for (let i = 0; i < data.messages.length; i++) {
            if (data.messages[i].msg_from === "Я: ") {
              let div_element_d_flex = document.createElement("div")
              div_element_d_flex.setAttribute("class", "d-flex flex-row justify-content-end mb-4 pt-1")
              let div_element = document.createElement("div")
              let flag = 0
              for (let j = i; j < data.messages.length; j++) {
                flag++
                if (data.messages[j].msg_from === "Я: ") {
                  let p1 = document.createElement("p")
                  p1.setAttribute("class", "small p-2 me-3 mb-1 text-white rounded-3 bg-info")
                  p1.textContent = data.messages[j].msg_text
                  div_element.appendChild(p1)
                } else {
                  i = i + flag - 2
                  break
                }
                if (j === data.messages.length - 1) {
                  i = data.messages.length
                  break
                }
              }
              let image = document.createElement("img")
              image.src = "https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava2-bg.webp"
              image.alt = ""
              image.style = "width: 45px; height: 100%;"
              div_element_d_flex.appendChild(div_element)
              div_element_d_flex.appendChild(image)
              div_card_body.appendChild(div_element_d_flex)
            } else {
              let div_element_d_flex = document.createElement("div")
              div_element_d_flex.setAttribute("class", "d-flex flex-row justify-content-start")
              let image = document.createElement("img")
              image.src = "https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava5-bg.webp"
              image.alt = ""
              image.style = "width: 45px; height: 100%;"
              let div_element = document.createElement("div")
              let flag = 0
              for (let j = i; j < data.messages.length; j++) {
                flag++
                if (data.messages[j].msg_from !== "Я: ") {
                  let p1 = document.createElement("p")
                  p1.setAttribute("class", "small p-2 ms-3 mb-1 rounded-3")
                  p1.style = "background-color: #f5f6f7;"
                  p1.textContent = data.messages[j].msg_text
                  div_element.appendChild(p1)
                } else {
                  i = i + flag - 2
                  break
                }
                if (j === data.messages.length - 1) {
                  i = data.messages.length
                  break
                }
              }
              div_element_d_flex.appendChild(image)
              div_element_d_flex.appendChild(div_element)
              div_card_body.appendChild(div_element_d_flex)

            }
          }
        }
      }
    );

  // 6
  let div_container = document.createElement("div")
  div_container.setAttribute("class", "container")
  // 7
  let div_row = document.createElement("div")
  div_row.setAttribute("class", "row card-footer text-muted align-items-center")
  // 8
  let div_column1 = document.createElement("div")
  div_column1.setAttribute("class", "col-md-10")
  // 9
  let textarea = document.createElement("textarea")
  textarea.id = "textarea" + chat_id
  textarea.setAttribute("class", "shoutbox-name form-control form-control-lg")
  textarea.setAttribute("type", "text")
  textarea.setAttribute("placeholder", "Введите сообщение")
  // 10
  let div_column2 = document.createElement("div")
  div_column2.setAttribute("class", "col-md-1")
  div_column2.style = "padding: 0 0 0 10px"
  // 11
  let a1 = document.createElement("a")
  a1.setAttribute("class", "ms-1 text-muted")
  a1.setAttribute("href", "#!")
  // 12
  let i1 = document.createElement("i")
  i1.setAttribute("class", "fas fa-paperclip")
  // 13
  let div_column3 = document.createElement("div")
  div_column3.setAttribute("class", "col-md-1")
  // 14
  let a2 = document.createElement("a")
  a2.setAttribute("class", "ms-3 link-info")
  a2.setAttribute("href", "#!")
  a2.addEventListener("click", function () {
    var input = document.getElementById("textarea" + chat_id)
    if (input.value !== ""){
      $.ajax({
        url: '/send_message',
        method: 'post',
        dataType: 'html',
        contentType:'application/json',
        data: JSON.stringify({"msg_text": input.value, "msg_to": user_with_id}),
        success: function(data){
          input.value = ""
        },
        error: function(data){
          console.log(data.responseText);
        }
      });
    }
  });

  // 15
  let i2 = document.createElement("i")
  i2.setAttribute("class", "fas fa-paper-plane")
  // Соединяем элементы
  a2.appendChild(i2)
  div_column3.appendChild(a2)
  a1.appendChild(i1)
  div_column2.appendChild(a1)
  div_column1.appendChild(textarea)
  div_row.appendChild(div_column1)
  div_row.appendChild(div_column2)
  div_row.appendChild(div_column3)
  div_container.appendChild(div_row)
  div_card.appendChild(button_exit)
  div_card.appendChild(div_card_body)
  div_card.appendChild(div_container)
  div_add.appendChild(div_card) // !
  // 16
  let br = document.createElement("br")
  // 17
  let a = document.createElement("a")

  a.setAttribute("data-mdb-toggle", "collapse")
  a.setAttribute("href", href)
  a.setAttribute("role", "button")
  a.setAttribute("aria-expanded", "false")
  // 18
  let div_card_body2 = document.createElement("div")
  div_card_body2.setAttribute("class", "card-body")
  // 19
  let div_card_pos = document.createElement("div")
  div_card_pos.setAttribute("class", "position-relative position-relative-example")
  // 20
  let div_card_pos_1 = document.createElement("div")
  div_card_pos_1.setAttribute("class", "position-absolute top-0 end-0 text-muted")
  let time_correct = new Date(time)
  let today = new Intl.DateTimeFormat('ru', {weekday: 'long'}).format(time_correct);
  let seconds = ""
  if (time_correct.getSeconds() < 10){
    seconds = "0" + time_correct.getSeconds()
  }
  else{
    seconds = time_correct.getSeconds()
  }
  div_card_pos_1.textContent = today + " " + time_correct.getHours() + ":" + seconds
  div_card_pos_1.style = "font-size: 75%"
  // 21 Уведомление!
  let div_card_pos_2 = document.createElement("div")
  if (checked === true){
    a.setAttribute("class", "card elements opacity-75")
  }else{
    a.setAttribute("class", "card elements")
    div_card_pos_2.setAttribute("class", "position-absolute top-0 start-50 text-warning")
    div_card_pos_2.textContent = "Уведомление!"
    div_card_pos_2.style = "font-size: 75%"
  }
  // 22
  let div_container2 = document.createElement("div")
  div_container2.setAttribute("class", "container")
  // 23
  let div_row2 = document.createElement("div")
  div_row2.setAttribute("class", "row")
  // 24
  let div_col1 = document.createElement("div")
  div_col1.setAttribute("class", "col-md-2")
  div_col1.style = "padding: 10px 0 10px 0"
  // 25
  let img = document.createElement("img")
  img.setAttribute("src", "https://blog.getbootstrap.com/assets/img/2022/05/docs-home.png")
  img.setAttribute("alt", "")
  img.setAttribute("class", "rounded-circle")
  img.style = "width: 45px; height: 45px"
  // 26
  let div_col2 = document.createElement("div")
  div_col2.setAttribute("class", "col-md-10")
  div_col2.style = "padding: 10px 0 0 10px"
  // 27
  let p1 = document.createElement("p")
  p1.setAttribute("class", "fw-bold mb-1 lang text-muted")
  p1.textContent = user_with
  // 28
  let div_flex = document.createElement("div")
  div_flex.setAttribute("class", "d-flex")
  // 29
  let span = document.createElement("div")
  span.setAttribute("class", "text-muted lang fw-bold")
  span.style = "font-size: 75%"
  span.textContent = from_who + ":"
  // 30
  let p2 = document.createElement("p")
  p2.setAttribute("class", "lang text-muted text-truncate")
  p2.style = "font-size: 75%"
  p2.textContent = last_message
  // Соединяем
  div_col2.appendChild(p1)
  div_flex.appendChild(span)
  div_flex.appendChild(p2)
  div_col2.appendChild(div_flex)
  div_col1.appendChild(img)
  div_row2.appendChild(div_col1)
  div_row2.appendChild(div_col2)
  div_container2.appendChild(div_row2)
  div_card_pos.appendChild(div_card_pos_1)
  div_card_pos.appendChild(div_card_pos_2)
  div_card_body2.appendChild(div_card_pos)
  div_card_body2.appendChild(div_container2)
  a.appendChild(div_card_body2) // !
  let div_main = document.createElement("div")
  div_main.appendChild(div_add)
  div_main.appendChild(br)
  div_main.appendChild(a)
  return div_main
}


  $('.shoutbox-name').emojioneArea({
    emojiPlaceholder: ":smile_cat:",
    searchPlaceholder: "Поиск",
    buttonTitle: "Эмодзи",
    searchPosition: "top",
    pickerPosition: "top"
  });

$(function() {
  $('.translate').click(function() {
    let lang = $(this).attr('id');
      change_language(lang);
  });
});

let lang = localStorage.getItem('language');
change_language(lang);
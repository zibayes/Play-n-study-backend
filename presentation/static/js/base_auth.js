// Отображение чата, если нет сообщений. Удаление сообщений, редактирование сообщений, удаление диалога.
import {
    change_language,
    translate
} from './test_constructor_functions.js';
function selectElementContents(el) {
    var range = document.createRange();
    range.selectNodeContents(el);
    var sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
}
let bg = document.querySelector('.mouse-parallax-bg');
window.addEventListener('mousemove', function(e) {
    let x = e.clientX / window.innerWidth;
    let y = e.clientY / window.innerHeight;
    bg.style.transform = 'translate(-' + x * 150 + 'px, -' + y * 150 + 'px)';
});

let div_main = document.getElementsByClassName('chats')[0]

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
      let div = add_element_chat(json_data.chats[i].chat_id, json_data.chats[i].time, json_data.chats[i].user_with, json_data.chats[i].from_who, json_data.chats[i].last_message, json_data.chats[i].checked, json_data.chats[i].user_with_id, json_data.chats[i].msg_new_count, json_data.chats[i].from_who_id)
      div_main.appendChild(div)
    }
  },

});
function click(e) {
  const container = document.querySelector(".menu_board_detail")
  if (!container?.contains(e.target)){
    document.querySelector(".menu_board_detail")?.remove()
    document.removeEventListener("click", click)
  }
}
function click2(e) {
  const container = document.querySelector(".menu_board_detail2")
  if (!container?.contains(e.target)){
    document.querySelector(".menu_board_detail2")?.remove()
    document.removeEventListener("click", click)
  }
}
function chat_message_div(message) {
  let div_element_d_flex = document.createElement("div")
  let div_menu_board = document.createElement("div")

  if (message.msg_from === "Я") {
      div_element_d_flex.setAttribute("class", "d-flex flex-row justify-content-end mb-4 pt-1")
      let p1 = document.createElement("p")
      div_element_d_flex.addEventListener("contextmenu", function (e) {
        p1.contentEditable = "false"
        event.preventDefault()
        document.querySelector(".menu_board_detail")?.remove()
        document.querySelector(".menu_board_detail2")?.remove()
        document.addEventListener("click", click)
        let div_menu_board_detail = document.createElement("div")
        let ul_drop_item = document.createElement("ul")
        let li_drop_item1 = document.createElement("li")
        let li_drop_item2 = document.createElement("li")
        let button_link1 = document.createElement("button")
        let button_link2 = document.createElement("button")
        let span_text_drop_item1 = document.createElement("span")
        let span_text_drop_item2 = document.createElement("span")
        div_menu_board.setAttribute("class", 'menu_board')
        div_menu_board_detail.setAttribute("class", 'menu_board_detail')
        ul_drop_item.setAttribute("class", 'ul_dropitem')
        li_drop_item1.setAttribute("class", "li_dropitem")
        li_drop_item2.setAttribute("class", "li_dropitem")
        button_link1.setAttribute("class", "link_item")
        button_link2.setAttribute("class", "link_item")
        span_text_drop_item1.setAttribute("class", "text_dropitem")
        span_text_drop_item1.textContent = "Удалить сообщение"
        span_text_drop_item2.setAttribute("class", "text_dropitem")
        span_text_drop_item2.textContent = "Редкатировать сообщение"
        button_link1.addEventListener("click", function () {
          $.ajax({
            url: '/remove_message/' + message.msg_id,
            method: 'post',
            dataType: 'json',
          })
          div_menu_board_detail.remove()
          div_element_d_flex.remove()
        })
        button_link2.addEventListener("click", function () {
          p1.contentEditable = 'true'
          div_menu_board_detail.remove()
          selectElementContents(p1)
          let div_menu_board_detail_dop = document.createElement("div")
          let ul_drop_item = document.createElement("ul")
          let li_drop_item = document.createElement("li")
          let button_link = document.createElement("button")
          button_link.addEventListener("click", function () {
              p1.contentEditable = "false"
              div_menu_board_detail_dop.remove()
              $.ajax({
                url: '/update_message/' + message.msg_id,
                method: "post",
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify({"msg_text": p1.innerHTML}),
            })
          })
          let span_text_drop_item = document.createElement("span")
          let li_drop_item2 = document.createElement("li")
          let button_link2 = document.createElement("button")
          button_link2.addEventListener("click", function () {
            p1.contentEditable = "false"
            div_menu_board_detail_dop.remove()
            p1.textContent = message.msg_text
          })
          let span_text_drop_item2 = document.createElement("span")

          div_menu_board_detail_dop.setAttribute("class", "menu_board_detail2")
          ul_drop_item.setAttribute("class", 'ul_dropitem')
          li_drop_item.setAttribute("class", "li_dropitem")
          button_link.setAttribute("class", "link_item")
          span_text_drop_item.setAttribute("class", "text_dropitem")
          li_drop_item2.setAttribute("class", "li_dropitem")
          button_link2.setAttribute("class", "link_item")
          span_text_drop_item2.setAttribute("class", "text_dropitem")
          span_text_drop_item.textContent = "Подтвердить"
          span_text_drop_item2.textContent = "Отмена"
          button_link.appendChild(span_text_drop_item)
          button_link2.appendChild(span_text_drop_item2)
          li_drop_item.appendChild(button_link)
          li_drop_item2.appendChild(button_link2)
          ul_drop_item.appendChild(li_drop_item)
          ul_drop_item.appendChild(li_drop_item2)
          div_menu_board_detail_dop.appendChild(ul_drop_item)
          div_menu_board.appendChild(div_menu_board_detail_dop)
        })
        button_link1.appendChild(span_text_drop_item1)
        button_link2.appendChild(span_text_drop_item2)
        li_drop_item1.appendChild(button_link1)
        li_drop_item2.appendChild(button_link2)
        ul_drop_item.appendChild(li_drop_item1)
        ul_drop_item.appendChild(li_drop_item2)
        div_menu_board_detail.appendChild(ul_drop_item)
        div_menu_board.appendChild(div_menu_board_detail)
      })
      let div_element = document.createElement("div")
      p1.setAttribute("class", "small p-2 me-3 mb-1 text-white rounded-3 bg-info")
      p1.textContent = message.msg_text
      div_element.appendChild(p1)
      let image = document.createElement("img")
      image.src = '/userava/' + message.msg_from_id
      image.alt = ""
      image.style = "width: 45px; height: 100%;border-radius: 50%;"
      div_element_d_flex.appendChild(div_element)
      div_element_d_flex.appendChild(image)
    } else {
      div_element_d_flex.setAttribute("class", "d-flex flex-row justify-content-start mb-4 pt-1")
      let image = document.createElement("img")
      image.src = '/userava/' + message.msg_from_id
      image.alt = ""
      image.style = "width: 45px; height: 100%;border-radius: 50%;"
      let div_element = document.createElement("div")
      let p1 = document.createElement("p")
      p1.setAttribute("class", "small p-2 ms-3 mb-1 rounded-3")
      p1.style = "background-color: #f5f6f7;"
      p1.textContent = message.msg_text
      div_element.appendChild(p1)
      div_element_d_flex.appendChild(image)
      div_element_d_flex.appendChild(div_element)

    }
  div_element_d_flex.appendChild(div_menu_board)
  return div_element_d_flex
}
function add_element_chat(chat_id, time, user_with, from_who, last_message, checked, user_with_id, msg_new_count, from_who_id) {
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
  button_exit.addEventListener("click", function () {
    div_card_body.innerHTML = ''
  })

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
  textarea.setAttribute("class", "shoutbox-name form-control form-control-lg")
  textarea.setAttribute("type", "text")
  textarea.setAttribute("id", "message_right")
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
  a2.setAttribute("class", "link-info")
  a2.setAttribute("id", "button_send_right")
  a2.style = "margin-left: -15px;"
  a2.setAttribute("href", "#!")
  a2.addEventListener("click", function () {
    if (textarea.value !== ""){
      $.ajax({
        url: '/send_message',
        method: 'post',
        dataType: 'json',
        contentType:'application/json',
        data: JSON.stringify({"msg_text": textarea.value, "msg_to": user_with_id}),
        success: function(data){
          p2.textContent = data.msg_text
          span.textContent = from_who + ":"

          textarea.value = ""
          div_card_body.appendChild(chat_message_div(data))
        },

      });
    }
  });

  var socket = io.connect('http://' + document.domain + ':' + location.port);

  socket.on( 'connect', function() {
    socket.emit( 'my event', {
      data: 'User Connected'
    } )
    document.getElementById('button_send_right').addEventListener("click", function( e ) {
      e.preventDefault()
      let user_input = $( '#message_right' ).val()
      socket.emit( 'my event', {
        from_who_id : from_who_id,
        msg_from_id : from_who_id,
        user_with_id : user_with_id,
        msg_text : user_input,
        msg_from: from_who,
        msg_date: new Date()
      } )
    } )
  } )
  socket.on( 'my response', function( msg ) {

    if( msg.from_who_id === user_with_id && msg.user_with_id === from_who_id ) {
        div_card_body.appendChild(chat_message_div(msg))
        span.textContent = user_with + ":"
        p2.textContent = msg.msg_text
    }
  })

  // 15
  let i2 = document.createElement("i")
  i2.setAttribute("class", "fas fa-paper-plane")
  // Соединяем элементы
  a2.appendChild(i2)
  div_column3.appendChild(a2)
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

  a.addEventListener("click", function () {
    $.ajax({
        url: '/get_dialog',
        method: 'post',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({"chat_id": chat_id}),
        success: function (data) {
          if (div_card_body.innerHTML !== ''){
              div_card_body.innerHTML = ''
              return
          }
          data.messages.forEach(function (entry) {
            let div_element_d_flex = chat_message_div(entry)
            div_card_body.appendChild(div_element_d_flex)
          })
        },

      }
    );
  })

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
  if (time !== ''){
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
  }


  div_card_pos_1.style = "font-size: 75%"
  // 21 Уведомление!
  let div_card_pos_2 = document.createElement("div")
  if (true === true){
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
  img.src = '/userava/' + user_with_id
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
function element_chat(chat_id, time, user_with, from_who, last_message, checked, user_with_id, msg_new_count, from_who_id) {
    let btn_del_chat = document.createElement("button")
    let li_chat = document.createElement("li")
    let a_element_chat = document.createElement("a")
    let div_element_chat = document.createElement("div")
    let img_element_chat = document.createElement('img')
    let div_element_chat_pt_message = document.createElement("div")
    let p_element_name = document.createElement("p")
    let p_element_message = document.createElement("p")
    let div_element_chat_pt_time = document.createElement("div")
    let p_element_time = document.createElement("p")
    let span_element_counter = document.createElement("span")

    btn_del_chat.setAttribute("class", 'delete_item delete_item_btn btn btn-secondary')
    btn_del_chat.style = "position: relative;height: 30px;width: 20px;text-align: center;display: flex;\n" +
        "    align-items: center;\n" +
        "    justify-content: center; top: 35px;left:100px"
    btn_del_chat.textContent = "✖"
    btn_del_chat.addEventListener("click", function () {
         $.ajax({
          url: '/remove_chat/' + chat_id,
          method: 'post',
          dataType: 'json'
        })
         li_chat.remove()
         ul_chat_item.innerHTML = ''

     })
    li_chat.setAttribute("class", "li_chat p-2 border-bottom li")
    li_chat.style = "border-radius: 15px;"
    a_element_chat.setAttribute("class", "d-flex justify-content-between")
    a_element_chat.setAttribute("href", "#!")
    div_element_chat.setAttribute("class", "d-flex flex-row")
    img_element_chat.setAttribute("class", "rounded-circle d-flex align-self-center me-3 shadow-1-strong")
    img_element_chat.style = "width: 60px"
    img_element_chat.src = '/userava/' + user_with_id
    div_element_chat_pt_message.setAttribute("class", "pt-1")
    p_element_name.setAttribute("class", "fw-bold mb-0")
    p_element_name.textContent = user_with
    p_element_message.id = chat_id
    p_element_message.setAttribute("class", "small text-muted")
    p_element_message.textContent = last_message
    div_element_chat_pt_time.setAttribute("class", "pt-1")
    p_element_time.setAttribute("class", "small text-muted mb-1 lang")
    if (time !== ''){
        let time_mes = new Intl.DateTimeFormat('ru', {weekday: 'long'}).format(new Date(time))
        let time_message_hour_sec = new Date(time)
        let time_message = new Date(time).getTime()
        let time_now = new Date().getTime()
        if (Math.floor(time_message / 1000) + 120 >= Math.floor(time_now / 1000)){
            p_element_time.textContent = 'сейчас'
            p_element_time.setAttribute("key", "just_now")
        }
        else {
            let sec = time_message_hour_sec.getSeconds() < 10 ?  '0' + time_message_hour_sec.getSeconds() : time_message_hour_sec.getSeconds()
            p_element_time.textContent = time_mes + " " + time_message_hour_sec.getHours() + ":" + sec + " "
        }
    }


    span_element_counter.setAttribute("class", "badge bg-danger float-end")
    span_element_counter.textContent = msg_new_count ===  0 ? null : msg_new_count

    a_element_chat.addEventListener("click" , function (event) {
        if (document.querySelector(".delete_item_btn") === null){
            return;
        }
        if (document.querySelector(".delete_item_btn").contains(event.target)){
            return
        }
        span_element_counter.textContent = null
        $.ajax({
          url: '/get_dialog',
          method: 'post',
          dataType: 'json',
          contentType: 'application/json',
          data: JSON.stringify({"chat_id": chat_id}),
          success: function (data) {
                data.messages.forEach(function (entry) {
                    let li_item = getLiItem(entry)
                    ul_chat_item.appendChild(li_item)

                })
          }
        })
        ul_chat_item.innerHTML = ''
        div_sent.innerHTML = ''
        let textarea = document.createElement("textarea")
        let btn_message = document.createElement("button")
        textarea.placeholder = "Message"
        textarea.id = "message"
        textarea.setAttribute("class", "form-control langp")
        textarea.setAttribute("key", "message")
        textarea.rows = '4'
        btn_message.type = "button"
        btn_message.id = "button_send"
        btn_message.setAttribute("class", "btn btn-info btn-rounded float-end lang")
        btn_message.setAttribute("key", "send")
        btn_message.style = "margin-top: 10px;"
        btn_message.textContent = "Send"
        btn_message.addEventListener("click", function () {
            if (textarea.value !== ''){
                $.ajax({
                    url: '/send_message',
                    method: "post",
                    dataType: 'json',
                    contentType: 'application/json',
                    data: JSON.stringify({"msg_text": textarea.value, "msg_to": user_with_id}),
                    success: function (data){
                        textarea.value = ""
                        ul_chat_item.appendChild(getLiItem(data))
                        p_element_message.textContent = data.msg_text
                    }
                })
            }
        })
        div_sent.appendChild(textarea)
        div_sent.appendChild(btn_message)

          var socket = io.connect('http://' + document.domain + ':' + location.port);

          socket.on( 'connect', function() {
            socket.emit( 'my event', {
              data: from_who_id
            } )
            document.getElementById('button_send').addEventListener("click", function( e ) {
              e.preventDefault()
              let user_input = $( '#message' ).val()
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
                ul_chat_item.appendChild(getLiItem(msg))
                p_element_message.textContent = msg.msg_text
            }
          })
    })
    
    div_element_chat_pt_time.appendChild(p_element_time)
    div_element_chat_pt_time.appendChild(span_element_counter)

    div_element_chat_pt_message.appendChild(p_element_name)
    div_element_chat_pt_message.appendChild(p_element_message)

    div_element_chat.appendChild(img_element_chat)
    div_element_chat.appendChild(div_element_chat_pt_message)

    a_element_chat.appendChild(div_element_chat)
    a_element_chat.appendChild(btn_del_chat)
    a_element_chat.appendChild(div_element_chat_pt_time)

    li_chat.appendChild(a_element_chat)

    return li_chat
}
function selectElementContents(el) {
    var range = document.createRange();
    range.selectNodeContents(el);
    var sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
}
function click(e) {
  const container = document.querySelector(".menu_board_detail_message")
  if (!container?.contains(e.target)){
    document.querySelector(".menu_board_detail_message")?.remove()
    document.removeEventListener("click", click)
  }
}
function getLiItem(message){
    let div_w_100 = document.createElement("div")
    let delete_item = document.createElement('button');
    delete_item.textContent = "✖"
    delete_item.style ="position: relative;height: 30px;width: 20px;text-align: center;display: flex;\n" +
        "    align-items: center;\n" +
        "    justify-content: center;"
    let li_item = document.createElement("li")
    let img_item = document.createElement("img")
    let div_card_item = document.createElement("div")
    let div_card_header_item = document.createElement("div")
    let p_item_name = document.createElement("p")
    let p_item_time = document.createElement("p")
    let i_item_time = document.createElement("i")
    let div_item_card_body = document.createElement("div")
    let p_item_text = document.createElement("p")
    div_w_100.setAttribute("class", "card w-100 message")
    let div_menu_board = document.createElement("div")
    div_w_100.addEventListener("contextmenu", function (e) {
        p_item_text.contentEditable = "false"
        event.preventDefault()
        document.querySelector(".menu_board_detail_message")?.remove()
        document.querySelector(".menu_board_detail_message2")?.remove()
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
        div_menu_board_detail.setAttribute("class", 'menu_board_detail_message')
        ul_drop_item.setAttribute("class", 'ul_dropitem')
        li_drop_item1.setAttribute("class", "li_dropitem")
        li_drop_item2.setAttribute("class", "li_dropitem")
        button_link1.setAttribute("class", "link_item")
        button_link2.setAttribute("class", "link_item")
        span_text_drop_item1.setAttribute("class", "text_dropitem")
        span_text_drop_item1.textContent = "Удалить сообщение"
        span_text_drop_item2.setAttribute("class", "text_dropitem")
        span_text_drop_item2.textContent = "Редактировать сообщение"
        button_link1.addEventListener("click", function () {
          $.ajax({
            url: '/remove_message/' + message.msg_id,
            method: 'post',
            dataType: 'json',
          })

          div_menu_board_detail.remove()
          div_w_100.remove()
            img_item.remove()
        })
        button_link2.addEventListener("click", function () {
          p_item_text.contentEditable = 'true'
          div_menu_board_detail.remove()
          selectElementContents(p_item_text)
          let div_menu_board_detail_dop = document.createElement("div")
          let ul_drop_item = document.createElement("ul")
          let li_drop_item = document.createElement("li")
          let button_link = document.createElement("button")
          button_link.addEventListener("click", function () {
              p_item_text.contentEditable = "false"
              div_menu_board_detail_dop.remove()

              $.ajax({
                url: '/update_message/' + message.msg_id,
                method: "post",
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify({"msg_text": p_item_text.innerHTML}),
            })
          })
          let span_text_drop_item = document.createElement("span")
          let li_drop_item2 = document.createElement("li")
          let button_link2 = document.createElement("button")
          button_link2.addEventListener("click", function () {
            p_item_text.contentEditable = "false"
              p_item_text.textContent = message.msg_text
            div_menu_board_detail_dop.remove()
          })
          let span_text_drop_item2 = document.createElement("span")
          div_menu_board_detail_dop.setAttribute("class", "menu_board_detail_message2")
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
    div_w_100.appendChild(div_menu_board)
    li_item.setAttribute("class", "d-flex mb-4")
    img_item.setAttribute("class", "")
    img_item.style = "width: 60px"

    div_card_item.setAttribute("class", "card  message")
    div_card_header_item.setAttribute("class", "card-header d-flex justify-content-between p-3")
    p_item_name.setAttribute("class", "fw-bold mb-0")
    p_item_name.textContent = message.msg_from

    p_item_time.setAttribute("class", "text-muted small mb-0")

    let time = new Intl.DateTimeFormat('ru', {weekday: 'long'}).format(new Date(message.msg_date))


    if (new Date(message.msg_date).getSeconds() < 10){
        p_item_time.textContent = time + " " + new Date(message.msg_date).getHours() + ":0" + new Date(message.msg_date).getSeconds() + ' '
    }else{
        p_item_time.textContent = time + " " + new Date(message.msg_date).getHours() + ":" + new Date(message.msg_date).getSeconds() + " "
    }
    i_item_time.setAttribute("class", "far fa-clock")
    div_item_card_body.setAttribute("class", "card-body")
    p_item_text.setAttribute("class", "mb-0")
    p_item_text.textContent = message.msg_text



    if (message.msg_from !== "Я"){
        img_item.setAttribute("class", "rounded-circle d-flex align-self-start shadow-1-strong me-3")
        img_item.src = '/userava/' + message.msg_from_id
        div_item_card_body.style = "width: 350px"
        div_item_card_body.appendChild(p_item_text)
        p_item_time.appendChild(i_item_time)
        div_card_header_item.appendChild(p_item_name)

        div_card_header_item.appendChild(p_item_time)
        div_card_item.appendChild(div_card_header_item)
        div_card_item.appendChild(div_item_card_body)
        li_item.appendChild(img_item)
        li_item.appendChild(div_card_item)
    }else{
        img_item.setAttribute("class", "rounded-circle d-flex align-self-start shadow-1-strong ms-3")
        img_item.src = '/userava/' + message.msg_from_id
        div_w_100.style = "margin-left: 150px"
        div_item_card_body.appendChild(p_item_text)
        p_item_time.appendChild(i_item_time)
        div_card_header_item.appendChild(p_item_name)

        div_card_header_item.appendChild(p_item_time)
        div_w_100.appendChild(div_card_header_item)
        div_w_100.appendChild(div_item_card_body)
        li_item.appendChild(div_w_100)
        li_item.appendChild(img_item)
    }
    return li_item

}
let ul_chat_item = document.getElementById("ul_chat_item")
let div_sent = document.getElementById("send_message_form")
let ul_chat = document.getElementById("ul_chat")

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
      let li = element_chat(json_data.chats[i].chat_id, json_data.chats[i].time, json_data.chats[i].user_with, json_data.chats[i].from_who, json_data.chats[i].last_message, json_data.chats[i].checked, json_data.chats[i].user_with_id, json_data.chats[i].msg_new_count, json_data.chats[i].from_who_id)
      ul_chat.appendChild(li)
    }
  }
});

// chat
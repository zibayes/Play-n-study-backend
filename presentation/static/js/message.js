let ul_chat_item = document.getElementById("ul_chat_item")
let ul_chat = document.getElementById("ul_chat")

function element_chat(chat_id, time, user_with, from_who, last_message, checked, user_with_id) {

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

    li_chat.setAttribute("class", "p-2 border-bottom li")
    li_chat.style = "border-radius: 15px;"
    a_element_chat.setAttribute("class", "d-flex justify-content-between")
    a_element_chat.setAttribute("href", "#!")
    div_element_chat.setAttribute("class", "d-flex flex-row")
    img_element_chat.setAttribute("class", "rounded-circle d-flex align-self-center me-3 shadow-1-strong")
    img_element_chat.style = "width: 60px"
    img_element_chat.src = "https://mdbcdn.b-cdn.net/img/Photos/Avatars/avatar-8.webp"
    div_element_chat_pt_message.setAttribute("class", "pt-1")
    p_element_name.setAttribute("class", "fw-bold mb-0")
    p_element_name.textContent = from_who
    p_element_message.setAttribute("class", "small text-muted")
    p_element_message.textContent = last_message
    div_element_chat_pt_time.setAttribute("class", "pt-1")
    p_element_time.setAttribute("class", "small text-muted mb-1")
    p_element_time.textContent = time
    span_element_counter.setAttribute("class", "badge bg-danger float-end")
    span_element_counter.textContent = checked? null : 1

    a_element_chat.addEventListener("click" , function () {
        $.ajax({
          url: '/get_dialog',
          method: 'post',
          dataType: 'json',
          contentType: 'application/json',
          data: JSON.stringify({"chat_id": chat_id}),
          success: function (data) {
                ul_chat_item.innerHTML = ''

                data.messages.forEach(function (entry) {
                    let li_item = getLiItem(entry)
                    ul_chat_item.appendChild(li_item)
                })

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
    a_element_chat.appendChild(div_element_chat_pt_time)

    li_chat.appendChild(a_element_chat)

    return li_chat
}

function getLiItem(message){
    let div_w_100 = document.createElement("div")

    let li_item = document.createElement("li")
    let img_item = document.createElement("img")
    let div_card_item = document.createElement("div")
    let div_card_header_item = document.createElement("div")
    let p_item_name = document.createElement("p")
    let p_item_time = document.createElement("p")
    let i_item_time = document.createElement("i")
    let div_item_card_body = document.createElement("div")
    let p_item_text = document.createElement("p")

    div_w_100.setAttribute("class", "card w-100")

    li_item.setAttribute("class", "d-flex mb-4")
    img_item.setAttribute("class", "")
    img_item.style = "width: 60px"
    img_item.src = "https://mdbcdn.b-cdn.net/img/Photos/Avatars/avatar-8.webp"
    div_card_item.setAttribute("class", "card")
    div_card_header_item.setAttribute("class", "card-header d-flex justify-content-between p-3")
    p_item_name.setAttribute("class", "fw-bold mb-0")
    p_item_name.textContent = message.msg_from
    p_item_time.setAttribute("class", "text-muted small mb-0")
    let time = new Intl.DateTimeFormat('ru', {weekday: 'long'}).format(new Date(message.msg_date))

    p_item_time.textContent = time + " " + new Date(message.msg_date).getHours() + ":" + new Date(message.msg_date).getSeconds() + " "
    i_item_time.setAttribute("class", "far fa-clock")
    div_item_card_body.setAttribute("class", "card-body")
    p_item_text.setAttribute("class", "mb-0")
    p_item_text.textContent = message.msg_text

    if (message.msg_from === "Я: "){
        img_item.setAttribute("class", "rounded-circle d-flex align-self-start shadow-1-strong me-3")
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
        div_w_100.style = "margin-left: 20px"
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
      let li = element_chat(json_data.chats[i].chat_id, json_data.chats[i].time, json_data.chats[i].user_with, json_data.chats[i].from_who, json_data.chats[i].last_message, json_data.chats[i].checked, json_data.chats[i].user_with_id)
      ul_chat.appendChild(li)
    }
  }
});

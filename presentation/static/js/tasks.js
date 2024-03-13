var flag_id = 0
  $("#save").click(function (event){
    flag_id++
    let div = document.getElementById("notes")
    let name = $('#recipient-name').val()
    let message = $("#message-text").val()
    let date = new Date();
    console.log(date)
    console.log(date.getUTCDate())
    console.log(date.getUTCMonth())

    let div_add = document.createElement("div")
    div_add.id = flag_id
    div_add.setAttribute("class", "container col-md-3 mt-5")
    let div_element = document.createElement("div")
    div_element.setAttribute("class", "toast show fade mx-auto")
    div_element.setAttribute("role", "alert")
    div_element.setAttribute("aria-live", "assertive")
    div_element.setAttribute("aria-atomic", "true")
    div_element.setAttribute("data-mdb-autohide", "false")
    div_element.id = "static-example1"
    let div_toast = document.createElement("div")
    div_toast.setAttribute("class", "toast-header toast-primary")
    let strong = document.createElement("strong")
    strong.setAttribute("class", "me-auto lang")
    strong.setAttribute("key", "form")
    strong.setAttribute("style", "max-width:150px; word-wrap:break-word;")
    strong.textContent = name
    let small = document.createElement("small")
    small.setAttribute("style", "text-align: right")
    small.innerHTML = ((date.getUTCDate() < 10)?"0":"") + date.getUTCDate() + "-" + (((date.getUTCMonth()+1) < 10)?"0":"") + (date.getUTCMonth()+1) + "-" + date.getUTCFullYear() + " <br> " + ((date.getHours() < 10)?"0":"") + date.getHours() + ":" + ((date.getMinutes() < 10)?"0":"") + date.getMinutes() + ":" + ((date.getSeconds() < 10)?"0":"") + date.getSeconds()
    let button = document.createElement("button")
    button.id = "buttons"
    button.name = flag_id
    button.type = "button"
    button.setAttribute("class", "btn-close")
    button.setAttribute("data-mdb-dismiss", "toast")
    button.setAttribute("aria-label", "Close")
    button.setAttribute("onclick", "removeElement(this.name)")
    let button_edit = document.createElement("button")
    button_edit.id = "buttons_edit-" + flag_id
    button_edit.name = flag_id
    button_edit.type = "button"
    button_edit.setAttribute("class", "btn btn-transparent shadow-none")
    button_edit.setAttribute("style", "background-color: transparent; border-color: transparent; max-width: 5px; padding: 10px;")
    button_edit.setAttribute("data-mdb-dismiss", "toast")
    button_edit.setAttribute("aria-label", "Edit")
    button_edit.setAttribute("onclick", "removeElement(this.name)")
    button_edit.innerHTML = `<i class="fa fa-edit"></i>`
    let div_end = document.createElement("div")
    div_end.setAttribute("class", "toast_body")
    div_end.style = "padding: 8px; padding-bottom: 15px; margin: 15px; word-wrap:break-word;"
    div_end.textContent = message



    div_add.appendChild(div_element)
    div_element.appendChild(div_toast)
    div_toast.appendChild(strong)
    div_toast.appendChild(small)
    div_toast.appendChild(button_edit)
    div_toast.appendChild(button)
    div_element.appendChild(div_end)
    div.appendChild(div_add)

    $.ajax({
        url: '/add_note',
        method: "post",
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({"title": name, "text": message}),
        success: function (data){
            console.log(data)
          div_add.id = data
          button.name = data
        },
        error: function (data){
            console.log(data['responseText'])
        }
    })
  })

  function removeElement(index) {
    document.getElementById(index).remove()
    $.ajax({
        url: '/remove_note/' + index,
        method: "post",
        dataType: 'json',
        success: function (data){
            console.log(data)
          div_add.id = data
        },
        error: function (data){
            console.log(data['responseText'])
        }
    })
  }

  function editNote(index) {
    let wrapper = document.createElement('div')
    wrapper.setAttribute("style", "display: flex; justify-content: center;")

    let button_accept = document.createElement('button')
    button_accept.setAttribute("id", "button_accept-" + index)
    button_accept.setAttribute("type", "button")
    button_accept.setAttribute("class", "btn btn-success shadow-none")
    button_accept.setAttribute("style", "border-color: transparent; margin:8px; margin-top:3px;")
    button_accept.setAttribute("aria-label", "Edit")
    let icon_accept = document.createElement('i')
    icon_accept.setAttribute("class", "fa-solid fa-check")

    let button_decline = document.createElement('button')
    button_decline.setAttribute("id", "button_decline-" + index)
    button_decline.setAttribute("type", "button")
    button_decline.setAttribute("class", "btn btn-danger shadow-none")
    button_decline.setAttribute("style", "border-color: transparent; margin:8px; margin-top:3px;")
    button_decline.setAttribute("aria-label", "Edit")
    let icon_decline = document.createElement('i')
    icon_decline.setAttribute("class", "fa-solid fa-xmark")

    let note = document.getElementById(index)
    let input_text = document.createElement('textarea')
    let input_title = document.createElement('textarea')
    let title = document.getElementById('title-' + index)
    let text = document.getElementById('text-' + index)
    let edit_button = document.getElementById('buttons_edit-' + index)
    edit_button.setAttribute("hidden", "hidden")
    title.setAttribute("hidden", "hidden")
    text.setAttribute("hidden", "hidden")
    input_text.setAttribute("style", "margin: 16px; height: 40px; width: 87%; margin-bottom:6px;")
    input_text.setAttribute("name", "text")
    input_title.setAttribute("style", "margin: 6px; height: 40px; width: 60%;")
    input_title.setAttribute("name", "title")
    note.firstElementChild.firstElementChild.appendChild(input_text)
    button_accept.appendChild(icon_accept)
    button_decline.appendChild(icon_decline)
    wrapper.appendChild(button_accept)
    wrapper.appendChild(button_decline)
    note.firstElementChild.firstElementChild.appendChild(wrapper)
    note.firstElementChild.firstElementChild.firstElementChild.insertBefore(input_title, note.firstElementChild.firstElementChild.firstElementChild.firstElementChild)
    input_text.textContent = text.textContent
    input_title.textContent = title.textContent

    button_decline.addEventListener("click", function () {
        wrapper.remove()
        input_title.remove()
        input_text.remove()
        edit_button.removeAttribute("hidden")
        text.removeAttribute("hidden")
        title.removeAttribute("hidden")
    });

    button_accept.addEventListener("click", function () {
        text.textContent = input_text.value
        title.textContent = input_title.value
        $.ajax({
          url: '/update_note/' + index,
          method: "post",
          dataType: 'json',
          contentType: 'application/json',
          data: JSON.stringify({"title": input_title.value, "text": input_text.value}),
          success: function (data){
              console.log(data)
          },
          error: function (data){
              console.log(data['responseText'])
          }
        })
        wrapper.remove()
        input_title.remove()
        input_text.remove()
        edit_button.removeAttribute("hidden")
        text.removeAttribute("hidden")
        title.removeAttribute("hidden")
    });
  }
  window.editNote = editNote

  $('.datetimepicker').datetimepicker({
     locale: moment.locale('ru')
   });
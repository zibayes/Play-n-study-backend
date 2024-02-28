<!--Додумать удаление всего div'a и прикрепить к ним id-->
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
    button_edit.id = "buttons_edit"
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
<!--Додумать удаление всего div'a и прикрепить к ним id-->
  var flag_id = 0
  $("#save").click(function (event){
    flag_id++
    let div = document.getElementById("notes")
    let name = $('#recipient-name').val()
    let message = $("#message-text").val()

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
    strong.textContent = name
    let small = document.createElement("small")
    small.textContent = "0 mins ago"
    let button = document.createElement("button")
    button.id = "buttons"
    button.name = flag_id
    button.type = "button"
    button.setAttribute("class", "btn-close")
    button.setAttribute("data-mdb-dismiss", "toast")
    button.setAttribute("aria-label", "Close")
    button.setAttribute("onclick", "removeElement(this.name)")
    let div_end = document.createElement("div")
    div_end.setAttribute("class", "toast_body")
    div_end.style = "padding: 10px; margin: 35px;"
    div_end.textContent = message



    div_add.appendChild(div_element)
    div_element.appendChild(div_toast)
    div_toast.appendChild(strong)
    div_toast.appendChild(small)
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
/*
function getFile() {
    var form = $('#form2'),
        formData = new FormData()
        formParams = form.serializeArray();

    $.each(form.find('input[type="file"]'), function(i, tag) {
      $.each($(tag)[0].files, function(i, file) {
        formData.append(tag.name, file);
      });
    });

    $.each(formParams, function(i, val) {
      formData.append(val.name, val.value);
    });

    for (var pair of formData.entries()) {
        console.log(pair[0]+ ', ' + pair[1]);
    }
    alert(formData.get('file'))
}
function submit(){
    var url = "/create_course/{{user.user_id}}"
    var str1 = $("#form1").serialize();
    var form1 = $("#form1"),
        formData1 = new FormData()
    var form = $('#form2'),
        formData = new FormData()
    formParams = form1.serializeArray();

    $.each(form.find('input[type="file"]'), function(i, tag) {
      $.each($(tag)[0].files, function(i, file) {
        formData.append(tag.name, file);
        str1 += "&" + tag.name + "=" + file
      });
    });

    $.each(formParams, function(i, val) {
      formData.append(val.name, val.value);
    });

    $.ajax({
        url: "/create_course/{{user.user_id}}",
        type: "POST",
        dataType: "html",
        data: formData,
        processData: false,
        contentType: false,
        success: function (data, status)
        {
            console.log(status)
        },
        error: function (xhr, desc, err)
        {
            console.log(err, desc)
        }
    });

    // $.post(url, str1);
}
function submitBothForms() {
    const { form1, form2 } = document.forms;
    fetch(form1.action, {
        method: form1.method,
        headers: { "content-type": form1.enctype },
        body: new FormData(form1),
    });
    form2.submit();
}
submitForms = function(){
    document.getElementById("form1").submit();
    document.getElementById("form2").submit();
}
*/
var input = document.getElementById('textAreaExample')
input.oninput = function() {
    let width = $("#content").width() - 35;
    $.ajax({
        url: '/api/rendermd',
        method: 'post',
        dataType: 'html',
        contentType:'application/json',
        data: JSON.stringify({text: input.value}),
        success: function(data){
            document.getElementById('1').innerHTML = data.replace("img", "img style=\"max-width:" + width + "px;\"");
        }
    });

}
let event = new Event("input");
input.dispatchEvent(event);
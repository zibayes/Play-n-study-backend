var input = document.getElementById('textAreaExample')
input.oninput = function() {
    $.ajax({
        url: '/api/rendermd',
        method: 'post',
        dataType: 'html',
        contentType:'application/json',
        data: JSON.stringify({text: input.value}),
        success: function(data){
            document.getElementById('1').innerHTML = data;
        }
    });

}
input.textContent = `{{article.content}}`
let event = new Event("input");
input.dispatchEvent(event);
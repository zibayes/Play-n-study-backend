let add_comment_buttons = document.querySelectorAll(".addComment");
add_comment_buttons.forEach(elem =>{
    elem.addEventListener("click", function(e) {
        $('#' + elem.id).fadeOut(400);
        //elem.setAttribute("hidden", "hidden");
        let textareaComment = document.createElement('textarea');
        textareaComment.setAttribute('class', "form-control");
        textareaComment.setAttribute('placeholder', "Комментарий");
        textareaComment.setAttribute('maxlength', '5000');
        textareaComment.setAttribute('name', elem.id);
        textareaComment.setAttribute('id', "Comment-" + elem.id);
        textareaComment.setAttribute('rows', "2");
        textareaComment.setAttribute("hidden", "hidden");
        let divComment = document.getElementsByClassName(elem.id)[0];
        divComment.appendChild(textareaComment);
        setTimeout(() => {
            textareaComment.removeAttribute("hidden");
            $('#Comment-' + textareaComment.id).fadeIn(400);
        }, 400)
    });
})
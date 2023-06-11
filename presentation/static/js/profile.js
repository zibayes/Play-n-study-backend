flag = false
$("#subscribe-button").on("click", function () {
    if (flag === false){
        flag = true
        $(this).hide("slow", function () {
            $(this).text("Отписаться")
        })
        $(this).show("slow")
    } else{
        flag = false
        $(this).hide("slow", function () {
            $(this).text("Подписаться")
        })
        $(this).show("slow")
    }
})
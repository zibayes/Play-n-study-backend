<!--    var refresh = setInterval(backgr, 1000);-->
<!--    $("#div").hide()-->
<!--    var body_el = document.getElementById("body")-->
<!--    let color1 = Math.floor((Math.random() * 255) + 1);-->
<!--    let color2 = Math.floor((Math.random() * 255) + 1);-->
<!--    let color3 = Math.floor((Math.random() * 255) + 1);-->
<!--    let color4 = Math.floor((Math.random() * 255) + 1);-->
<!--    let color5 = Math.floor((Math.random() * 255) + 1);-->
<!--    let color6 = Math.floor((Math.random() * 255) + 1);-->

<!--    body_el.style.background = `radial-gradient(60% 80%, rgba(${color1},${color2},${color3},0.5), rgba(${color4}, ${color5}, ${color6},0.6 ))`;-->
<!--    var div = document.createElement("div")-->
<!--    div.style = "position: fixed; top: 50%;\n" +-->
<!--        "left: 50%;transform: translate(-50%, -50%);"-->
<!--    var div1 = document.createElement("div")-->
<!--    div1.style = "position: fixed; top: 40%;\n" +-->
<!--        "left: 50%;transform: translate(-50%, -50%);"-->
<!--    var el = document.createElement("i")-->
<!--    var text = document.createElement("h1")-->
<!--    text.textContent = "Сайт загружается, подождите"-->
<!--    text.style = "color: black; font-weight: bold;"-->
<!--    el.style = "color: black"-->
<!--    el.setAttribute("class", "fa fa-spinner fa-spin fa-3x fa-fw")-->
<!--    div.id = "2"-->
<!--    div1.id = "3"-->
<!--    div1.appendChild(text)-->
<!--    div.appendChild(el)-->
<!--    body_el.appendChild(div)-->
<!--    body_el.appendChild(div1)-->

<!--    var flag = true, body = document.body, pseudo = document.getElementById('pseudo-bg');-->
<!--    function backgr() {-->
<!--        let color1 = Math.floor((Math.random() * 255) + 1);-->
<!--        let color2 = Math.floor((Math.random() * 255) + 1);-->
<!--        let color3 = Math.floor((Math.random() * 255) + 1);-->
<!--        let color4 = Math.floor((Math.random() * 255) + 1);-->
<!--        let color5 = Math.floor((Math.random() * 255) + 1);-->
<!--        let color6 = Math.floor((Math.random() * 255) + 1);-->
<!--        if(flag){-->
<!--            body_el.style.background = `radial-gradient(60% 80%, rgba(${color1},${color2},${color3},0.5), rgba(${color4}, ${color5}, ${color6},0.6 ))`;-->
<!--            pseudo.style.opacity = 0;-->
<!--        }else{-->
<!--            pseudo.style.background = `radial-gradient(60% 80%, rgba(${color1},${color2},${color3},0.5), rgba(${color4}, ${color5}, ${color6},0.6 ))`;-->
<!--            pseudo.style.opacity = 1;-->
<!--        }-->
<!--        flag = !flag;-->
<!--    }-->
//    document.addEventListener( 'DOMContentLoaded', ()=> { // Ожидание готовности документа
<!--        $("#3").hide("slow", function () {-->
<!--            $("#3").remove()-->
<!--        })-->
<!--    })-->
//    document.addEventListener( 'DOMContentLoaded', ()=> { // Ожидание готовности документа
<!--        $("#2").hide('slow', function () {-->
<!--            this.remove()-->
<!--            body_el.style.background = "white"-->
<!--            pseudo.remove()-->
<!--            clearInterval(refresh)-->
<!--            $("#div").show("slow")-->
<!--        })-->
<!--    })-->
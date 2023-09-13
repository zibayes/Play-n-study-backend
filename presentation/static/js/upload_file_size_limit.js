let file = document.getElementById("customFile");
file.onchange = function() {
    if(this.files[0].size > 2097152){
       this.value = "";
    }
};
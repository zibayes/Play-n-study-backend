document.addEventListener( 'DOMContentLoaded', ()=>{ // Ожидание готовности документа
    document.querySelector('.my-div').scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });

});
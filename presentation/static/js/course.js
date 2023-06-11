$(function() {

    $(document).on({
        mouseover: function(event) {
            $(this).find('.far').addClass('star-over');
            $(this).prevAll().find('.far').addClass('star-over');
        },
        mouseleave: function(event) {
            $(this).find('.far').removeClass('star-over');
            $(this).prevAll().find('.far').removeClass('star-over');
        }
    }, '.rate');

    let isFirstTime = true
    $(document).on('click', '.rate', function() {
        if ( !$(this).find('.star').hasClass('rate-active') ) {
            $(this).siblings().find('.star').addClass('far').removeClass('fas rate-active');
            $(this).find('.star').addClass('rate-active fas').removeClass('far star-over');
            $(this).prevAll().find('.star').addClass('fas').removeClass('far star-over');

            rate_to_send = document.getElementById($(this).attr('id').substring(0, 5)).value.substring(4)
            url = '/api/set_rating/' + {{course.course_id}}
            $.ajax({
                url: url,
                method: 'post',
                dataType: 'html',
                contentType:'application/json',
                data: JSON.stringify({rate: rate_to_send}),
                success: function(data){
                    if(isFirstTime){
                        $('#feedback').fadeOut(400);
                    setTimeout(() => {
                        document.getElementById('feedback').innerHTML = data;
                        $('#feedback').fadeIn(400);
                        setTimeout(() => {
                            document.getElementById("feedback-comment").removeAttribute("hidden")
                        }, 0)
                        $('#feedback-comment').slideDown(400)
                    }, 400)
                        isFirstTime = false
                    }
                }
            });
        }
    });

});
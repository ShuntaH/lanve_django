 function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        let csrftoken = getCookie('csrftoken');

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

$(function () {
    const this_ = $(".like-btn");
    const likeUrl = this_.attr("data-href");
    $.ajax({
        url: likeUrl,
        method: "GET",
        data: {"status": 0},
        success: function (data) {
            if (data.liked) {
                this_.addClass("on");
                this_.removeClass("color-heart");
            }
        }, error: function (error) {
            console.log("error")
        }
    })
});
$(".like-btn").click(function (e) {
    e.preventDefault();
    const this_ = $(this);
    const like_cnt = $(".liked-cnt");
    const likeUrl = this_.attr("data-href");
    if (likeUrl) {
        $.ajax({
            url: likeUrl,
            method: "GET",
            data: {"status": 1},
            success: function (data) {
                let change_like = like_cnt.text();
                if (data.liked) {
                    like_cnt.text(++change_like);
                    this_.addClass("on color-heart");
                } else {
                    like_cnt.text(--change_like);
                    this_.removeClass("on");
                }
            }, error: function (error) {
                console.log("error")
            }
        })
    }
});
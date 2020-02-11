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
            }
        }, error: function (error) {
            console.log("error")
        }
    })
});
$(".like-btn").click(function (e) {
    e.preventDefault()
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
                    this_.addClass("on");
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
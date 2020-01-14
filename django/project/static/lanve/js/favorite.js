$(function () {
    // setup for ajax
    const csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    const favoriteList = [];// 連打防止用のコメントID格納リスト
    // いいねボタン押下時の処理
    onClickFavoriteLink();

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function onClickFavoriteLink() {
        $('.favorite-link').on('click', function () {
            let commentId = $(this).data('comment-id');
            let currentCount = $(this).data('count');
            let countViewer = $(this).find('.favorite_counter');
            if (favoriteList.indexOf(commentId) < 0) {
                favorite(commentId, currentCount, countViewer);
            } else if (favoriteList.indexOf(commentId) >= 0){
                delete_favorite(commentId, currentCount, countViewer);
            }
        });
    }

    // ajax通信して投票結果を反映する
    function favorite(commentId, currentCount, countViewer) {
        let url = '/api/v1/favorite/';
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                comment_id: commentId
            }
        }).then(
            data => {
                if (data.result) {
                    countViewer.text(currentCount + 1);
                    favoriteList.push(commentId);
                }
            },
            error => {
                if (error.responseJSON.message) {
                    alert(error.responseJSON.message);
                }
            }
        );
    }

    function delete_favorite(commentId, currentCount, countViewer) {
        let url = '/api/v1/delete_favorite/';
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                comment_id: commentId
            }
        }).then(
            data => {
                if (data.result) {
                    countViewer.text(currentCount);
                    const index = favoriteList.indexOf(commentId);
                    if (index > -1) {
                        favoriteList.splice(index, 1);
                    }
                }
            }
            ,
            error => {
                if (error.responseJSON.message) {
                    alert(error.responseJSON.message);
                }
            }
        );
    }
});



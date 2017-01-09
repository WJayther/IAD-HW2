function getCookie(name) {
    var cookieValue = null;
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

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(function() {
    $('.followBTN').click(function() {
        var id, fid;
        id =  cur_user_id;
        fid = $(this).attr('user_id');
        $.ajax({
            url: '/user/'+id+'/follows/'+fid,
            method: 'POST', // or another (GET), whatever you need
            data: {
                id: id, // data you need to pass to your function
                fid: fid
            },
            success: function (data) {        
                // success callback
                // you can process data returned by function from views.py
                alert(data)
            }
        });
    });
    $('.unfollowBTN').click(function() {
        var id, fid;
        id =  cur_user_id;
        fid = $(this).attr('user_id');
        $.ajax({
            url: '/user/'+id+'/unfollows/'+fid,
            method: 'POST', // or another (GET), whatever you need
            data: {
                id: id, // data you need to pass to your function
                fid: fid
            },
            success: function (data) {        
                // success callback
                // you can process data returned by function from views.py
                alert(data)
            }
        });
    });
});

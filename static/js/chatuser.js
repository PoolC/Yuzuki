var chat_user_ul = $("#chat-user-ul");
var chat_user_count = $("#user-count");

var process_user_items = function (data) {
    chat_user_ul.empty();
    for (var i = 0; i < data.length; i++) {
        var chat_item = data[i];
        var template = '<li class="chat-user row" id="list-user-{{user_id}}"><div class="chat-user-nickname col-xs-12"><a onclick="open_user_popup({{ user_id }})">{{user_nickname}}</a></div></li>';
        var rendered = Mark.up(template, chat_item);
        chat_user_ul.append(rendered);
    }
    chat_user_count.text(data.length + " 명");
};

var refresh_chat_user = function () {
    return $.ajax("/chat/user/data", {
        dataType: "json"
    }).done(process_user_items);
};

var wait_for_user_stream = function () {
    return $.ajax("/chat/user/stream", {
        cache: false
    }).done(function () {
        refresh_chat_user();
        wait_for_user_stream();
    }).fail(function (xhr) {
        if (xhr.status === 401 && !prompted_error) {
            prompted_error = true;
            alert("로그인 해야 합니다.");
            window.location.href = "/login?redirect=/chat";
        }
        if (xhr.status === 504) {
            // gateway timeout
            refresh_chat_user();
            wait_for_user_stream();
        } else {
            // any other error
            setTimeout(function () {
                refresh_chat_user();
                wait_for_user_stream();
            }, 10000);
        }
    });
};

setTimeout(function () {
    refresh_chat_user();
}, 100);
wait_for_user_stream();

$(window).on("pagehide unload", function () {
    $.ajax("/chat/user/out", {
        async: false
    });
});

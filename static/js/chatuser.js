var chat_user_ul = $("#chat-user-ul");
var chat_user_count = $("#user-count");

var process_user_items = function (data) {
    chat_user_ul.empty();
    for (var i = 0; i < data.length; i++) {
        var chat_item = data[i];
        var template = '<li class="chat-user row" id="{{user_id}}"><div class="chat-user-nickname col-xs-12">{{user_nickname}}</div></li>';
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
    return $.ajax("/chat/user/stream").done(function () {
        refresh_chat_user();
        wait_for_user_stream();
    }).fail(function () {
        refresh_chat_user();
        wait_for_user_stream();
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
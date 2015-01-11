var submit_lock = false;
var chat_input = $("#chat-input");
$("#chat-form").submit(function (e) {
    if (!submit_lock) {
        submit_lock = true;
        $.post("/chat/message/stream", $(this).serialize()).done(function () {
            chat_input.val("");
            submit_lock = false;
        });
    }
    return false;
});
var message_ul = $("#chat-message-ul");
var latest_uid = 1;

process_chat_items = function (data) {
    for (var i = 0; i < data.length; i++) {
        latest_uid = Math.max(latest_uid, data[i].uid);
        var chat_item = data[i];
        var template = '<li class="chat-item row" id="{{uid}}"><div id="{{user_id}}" class="chat-item-user-nickname col-xs-2">{{user_nickname}}</div><div class="chat-content-datetime col-xs-10"><span class="chat-content">{{content}}</span><span class="chat-datetime">{{created_at}}</div></li>';
        var rendered = Mark.up(template, chat_item);
        message_ul.append(rendered);
        if (message_ul.children().length > chat_per_page) {
            message_ul.children().first().remove();
        }
    }
};

get_newer_chat = function () {
    return $.ajax("/chat/message/data?id=" + latest_uid, {
        dataType: "json"
    }).done(process_chat_items);
};

wait_for_chat_stream = function () {
    $.ajax("/chat/message/stream").done(function () {
        get_newer_chat();
        wait_for_chat_stream();
    }).fail(function (xhr) {
        if (xhr.status == 401 && !prompted_error) {
            prompted_error = true;
            alert("로그인 해야 합니다.");
            window.location.href = "/login?redirect=/chat";
        }
        setTimeout(function () {
            get_newer_chat();
            wait_for_chat_stream();
        }, 10000);
    });
};
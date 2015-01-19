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

process_chat_items = function (data, enable_noti) {
    for (var i = 0; i < data.length; i++) {
        (function () {
            latest_uid = Math.max(latest_uid, data[i].uid);
            var chat_item = data[i];
            var template = '<li class="chat-item row" id="chat-{{uid}}"><div id="user-{{user_id}}" class="chat-item-user-nickname col-xs-2">{{user_nickname}}</div><div class="chat-content-datetime col-xs-10"><span class="chat-content">{{content}}</span><span class="chat-datetime">{{created_at}}</div></li>';
            var rendered = Mark.up(template, chat_item);
            message_ul.append(rendered);
            if (message_ul.children().length > chat_per_page) {
                message_ul.children().first().remove();
            }
            if (enable_noti === true && Notification.permission === "granted") {
                var contain_noti = chat_item.content.split(" ").some(function (content) {
                    return content === "@" + user_nickname;
                });
                if (contain_noti) {
                    var options = {
                        body: chat_item.content,
                        icon: "/favicon.ico"
                    };
                    var notification = new Notification(chat_item.user_nickname, options);
                    notification.onclick = function () {
                        window.focus();
                        var chat_selector = "#chat-" + chat_item.uid;
                        $(chat_selector).effect("highlight", 1500);
                    };
                }
            }
        })();
    }
};

get_newer_chat = function (enable_noti) {
    return $.ajax("/chat/message/data?id=" + latest_uid, {
        dataType: "json"
    }).done(function (data) {
        process_chat_items(data, enable_noti);
    });
};

wait_for_chat_stream = function () {
    $.ajax("/chat/message/stream").done(function () {
        get_newer_chat(true);
        wait_for_chat_stream();
    }).fail(function (xhr) {
        if (xhr.status === 401 && !prompted_error) {
            prompted_error = true;
            alert("로그인 해야 합니다.");
            window.location.href = "/login?redirect=/chat";
        }
        if (xhr.status === 504) {
            // gateway timeout
            get_newer_chat(true);
            wait_for_chat_stream();
        } else {
            // any other error
            setTimeout(function () {
                get_newer_chat(true);
                wait_for_chat_stream();
            }, 10000);
        }
    });
};

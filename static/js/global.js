var mobileVisible = false;

$(window).resize(function () {
    if ($(window).width() >= 768) {
        $(".sidebar").show();
    } else {
        if (mobileVisible) {
            $(".sidebar").show();
        } else {
            $(".sidebar").hide();
        }
    }
});

$(".menu-toggle").click(function () {
    if (mobileVisible) {
        $(".sidebar").hide(400);
        mobileVisible = false;
    } else {
        $(".sidebar").show(400);
        mobileVisible = true;
    }
});

var open_user_popup = function (user_id) {
    window.open("/profile/popup?user_id=" + user_id, "_blank", "fullscreen=no,titlebar=no,toolbar=no,directories=no,status=no,menubar=no,scrollbars=yes,resizable=yes,width=600,height=800");
};

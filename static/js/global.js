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
    console.log("hey");
    if (mobileVisible) {
        $(".sidebar").hide(400);
        mobileVisible = false;
    } else {
        $(".sidebar").show(400);
        mobileVisible = true;
    }
});
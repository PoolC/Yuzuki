var ok_sign = $(".password-confirm-ok");
var no_sign = $(".password-confirm-no");
var password = $("#password");
var password_confirm = $("#password_confirm");

ok_sign.hide();
no_sign.hide();
var show_password_validity_sign = function () {
    if (!password[0].validity.valid || password_confirm.val().length == 0) {
        ok_sign.hide();
        no_sign.hide();
    } else {
        password_confirm.attr("pattern", "^" + password.val() + "$");
        if (password_confirm.val() === password.val()) {
            ok_sign.show();
            no_sign.hide();
        } else {
            no_sign.show();
            ok_sign.hide();
        }
    }
};
$("#register-form").submit(function (e) {
    var password_hash = CryptoJS.SHA256($("#password").val()).toString();
    $("#password_real").val(password_hash);
    return true;
});
$("#password_confirm").on("input propertychange paste", show_password_validity_sign);
$("#password").on("input propertychange paste", show_password_validity_sign);
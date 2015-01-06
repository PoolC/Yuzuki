$("#login-form").submit(function (e) {
    var password_hash = CryptoJS.SHA256($("#password").val()).toString();
    $("#password-real").val(password_hash);
    return true;
});
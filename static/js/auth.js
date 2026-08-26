function logout() {
    $.ajax({
        type: "POST",
        url: "/api/auth/logout",
        success: function (response) {
            if (response.result === "success") {
                alert(response.msg);
                window.location.href = "/login";
            }
        }
    });

}
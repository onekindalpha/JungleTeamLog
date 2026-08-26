function login() {
    let email = $('#user-email').val();
    let password = $('#user-password').val();

    if (!email || !password) {
        alert('이메일과 비밀번호를 모두 입력해주세요.');
        return;
    }

    $.ajax({
        type: "POST",
        url: "/api/auth/login",
        contentType: "application/json",
        data: JSON.stringify({
            email: email,
            password: password
        }),
        success: function (response) {
            if (response['result'] === 'success') {
                $.cookie('mytoken', response['token'], { path: '/' });
                alert("로그인 완료!")
                window.location.href = '/';
            } else {
                alert(response['msg']);
            }
        }
    });
}

function register() {
    $.ajax({
        type: "POST",
        url: "/api/auth/signup",
        contentType: "application/json",
        data: JSON.stringify({
            email: $('#email').val(),
            password: $('#password_hash').val(),
            name: $('#name').val()
        }),
        success: function (response) {
            if (response['result'] == 'success') {
                alert('회원가입이 완료되었습니다.')
                window.location.href = '/login'
            } else {
                alert(response['msg'])
            }
        }
    })
}
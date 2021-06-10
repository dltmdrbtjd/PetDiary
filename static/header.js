$(document).ready(function() {

    let token = $.cookie('mytoken');
    if (token !== undefined){
        token = JSON.parse(atob(token.split('.')[1]));
        $('#user_id').text(token.id + '님 환영합니다.')
    }
});

function logout() {
    $.removeCookie('mytoken', {path: '/'});
    location.reload();
    window.location.href = '/login';
}
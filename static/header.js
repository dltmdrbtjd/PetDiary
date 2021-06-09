$(document).ready(function() {
    const url_string = window.location.search;
    if(url_string.includes('token_expired')){
        $.removeCookie('mytoken', {path: '/'})
        const not_login_user_html = `
                <li class="nav-item">
                    <a class="nav-link" href="/login" style="cursor: pointer;">로그인</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/register" style="cursor: pointer;">회원가입</a>
                </li>
        `;
        $('#show_user_by_token').empty().append(not_login_user_html)
        $('#show_review_save_button_by_token').empty()
    }

    let token = $.cookie('mytoken');
    if (token !== undefined){
        token = JSON.parse(atob(token.split('.')[1]));
        $('#user_id').text(token.id + '님 환영합니다.')
    }
});

function logout() {
    $.removeCookie('mytoken', {path: '/'});
    window.location.href = '/login';
}
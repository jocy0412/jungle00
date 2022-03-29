// 회원가입
function insertFunc(){
    // 회원가입시 입력정보
    let username_val = $('#input_username').val();
    let id_val = $('#input_id').val();
    let password_val1 = $('#input_password1').val();
    let password_val2 = $('#input_password2').val();

    // 가입 양식에 파일들이 입력값이 없을 경우 에러 출력
    if((username_val && id_val && password_val1 && password_val2) == false ){
        alert('모든 입력 필드에 입력이 필요합니다.');
        return false
    }

    // 가입시 비밀번호 확인가 둘다 같지 않을 경우 에러 출력
    if(password_val1 != password_val2){
        alert('비밀번호가 같지 않습니다.');
        return false
    }

    $.ajax({
        type: "POST",
        url: "/insert",
        data: {'username_give':username_val, 'id_give':id_val, 'password_give':password_val1},
        success: function (response) {
            if(response["result"] == "success"){
                alert('회원가입 완료!');
                window.location.reload();
            } else {
                    alert('다른 이유로 실패 했습니다.');
            }

        }
    })
}

// 로그인
function loginFunc(){
    let id_val = $('#login_id').val();
    let password_val = $('#login_password').val();
    $.ajax({
        type: "POST",
        url: "/login",
        data: {'id_give':id_val, 'password_give':password_val},
        success: function (response) {
            if(response["result"] == "success"){
                alert('로그인 되었습니다!');
                window.location.reload();
            } else {
                if(response["result"] == "not"){
                    alert('아이디가 없습니다!');
                } else {
                    alert('비밀번호가 틀렸습니다');
                }
            }

        }
    })
}

// 로그아웃
function logoutFunc(){
    // $.removeCooke('mytoken');
    alert('로그아웃!');
    window.location.href='/login'
}

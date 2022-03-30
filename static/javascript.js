// 회원가입, 고객정보 데이터 입력
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
        url: "/api/register",
        data: {'username_give':username_val, 'id_give':id_val, 'pw_give':password_val1},
        success: function (response) {
            if(response["result"] == "success"){
                alert('회원가입 완료!');
                window.location.href='/'
            } else {
                    alert('이미 가입된 ID입니다.');
            }
        }
    })
}

// 중복확인
function doubleCheck(){
    let id_val = $('#input_id').val();
    $.ajax({
        type: "POST",
        url: "/api/doublecheck",
        data: {'id_give':id_val },
        success: function (response) {
            if(response["result"] == "success"){
                alert('사용 가능한 ID입니다.');
            } else {
                alert('이미 가입된 ID입니다.');
            }
        }
    })
}

// 로그인
function loginFunc(){
    let id_val = $('#login_id').val();
    let pw_val = $('#login_password').val();
    $.ajax({
        type: "POST",
        url: "/api/login",
        data: {'id_give':id_val, 'pw_give':pw_val},
        success: function (response) {
            if(response["result"] == "success"){

                // mytoken이라는 키 값으로 쿠키에 저장
                $.cookie('mytoken', response['token']);

                alert('로그인 되었습니다!');
                window.location.href='/main';
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

// 로그아웃 하기
function logoutFunc(){
    $.removeCookie('mytoken');
    alert('로그아웃!');
    window.location.href='/'
}
// 회원가입 페이지 가기
function registFunc(){
    window.location.href='/register'
}

// 메인으로 가기
function menuAddFunc(){
    window.location.href='/api/addpage'
}

// 메인으로 가기
function homeFunc(){
    window.location.href='/'
}

// list 기능 구현

// $(document).ready(function() {
//     $("#right").html("");
// });
  
function show(category) {
    // if (document.getElementsByName('first')){
    //     $(".first").hide();
    // }

    console.log("들어온 카테고리값: "+category)
    $.ajax({
    type: 'POST',
    url: '/api/show',
    data: {'category_give': category},
    success: function(response) {
        if (response['status'] == 1) {
        let lists = response['list'];
        for (let i = 0; i < lists.length; i++) {
            let list = lists[i];
            let foodName = list["food_name"];
            let foodCategory = list["food_category"];
            let shopName = list["shop_name"];
            let shopAddress = list["shop_address"];
            let shopImg = list["shop_img"];
            let like = list["like"];
            let hate = list["hate"];
            let foodCode = list["food_code"];

            let tempHtml = `<div id="${foodCategory}">${foodCategory} 추천 메뉴
                            <div id="card">
                                <p id="foodname">${foodName}</p>
                                <p id="storename">${shopName}</p>
                                <p id="address">주소 : ${shopAddress}</p>
                                <img src="${shopImg}">
                                <div class="field is-grouped">
                                    <p class="control">
                                        <input type="checkbox" name="category" id="좋아요" onclick="like(${foodCode})">좋아요
                                    </p>
                                    <p class="control">
                                        <input type="checkbox" name="category" id="싫어요" onclick="hate(${foodCode})">싫어요
                                    </p>
                                </div>
                                <p>좋아요 : ${like}개</p>
                                <p>싫어요 : ${hate}개</p>
                                <hr>
                            </div>
                            </div>`;
            $("#right").append(tempHtml);
        }
        } else {
        console.log('들어온 status', response['status'])
        console.log('들어온 category', response['category'])
        let category = response['category']
        $('#' + category).hide()
        }
    }
    });
}
  
function like(foodCode){

}

function hate(foodCode){

}

//  메뉴추가

function addMenu() {
    let food_name = $("#food_name").val();
    let food_category;
    let shop_name = $("#shop_name").val();
    let shop_address = $("#shop_address").val();
    let shop_img= $("#shop_img").val()
    // let shop_img= $("#shop_img").val().replace(/C:\\fakepath\\/i, '');
    // let shop_url = $("#shop_url").val();
    
    let checkObj = document.getElementsByName("category");
    let length = checkObj.length;
    let checked = 0;
  
    for (i = 0; i < length; i++) {
      if (checkObj[i].checked === true) {
        checked += 1;
        food_category = checkObj[i].getAttribute("id");
      }
    }
  
    if (checked >= 2){
      alert("메뉴 카테고리를 하나만 선택해주세요!");
      return false;
    }
  
    if (checked == 0){
      alert("메뉴 카테고리를 선택해주세요!");
      return false;
    }
  
    console.log(food_name);
    console.log(food_category);
    console.log(shop_img);
  
    // 메뉴 추가하기 요청
    $.ajax({
        type: "POST", // POST 방식으로 요청하겠다.
        url: "/api/add", // /add라는 url에 요청하겠다.
        data: {
               food_give: food_name,
               category_give: food_category,
               shop_name_give: shop_name,
               shop_address_give: shop_address,
               shop_img_give: shop_img
              }, // 데이터를 주는 방법
        success: function (response) { // 성공하면
            if (response["result"] == "success") {
                alert("메뉴 추가에 성공했습니다!");
                // 3. 성공 시 페이지 새로고침하기
                window.location.href='/main'
            } 
            if (response["result"] == "insertfail") {
                alert("메뉴 추가에 실패했습니다!");
                window.location.reload();
            }
        }
    })
}
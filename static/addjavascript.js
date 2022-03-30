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
              window.location.reload();
          } 
          if (response["result"] == "insertfail") {
              alert("메뉴 추가에 실패했습니다!");
              window.location.reload();
          }
      }
  })
}
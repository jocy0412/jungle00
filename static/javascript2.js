$(document).ready(function() {
  $("#right").html("");
});

function show(category) {
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



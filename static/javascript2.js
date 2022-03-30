$(document).ready(function() {
  $("#right").html("");
});

function showKor() {
  $("#right").empty();
  let checkKor = $("#한식").is(":checked");
  if (checkKor) {
    $.ajax({
      type: "GET",
      url: "/api/kor",
      data: {},
      success: function(response) {
        let kors = response["kor_list"];
        for (let i = 0; i < kors.length; i++) {
          let kor = kors[i];
          let foodName = kor["food_name"];
          let foodCategory = kor["food_category"];
          let shopName = kor["shop_name"];
          let shopAddress = kor["shop_address"];
          let shopImg = kor["shop_img"];
          let like = kor["like"];
          let hate = kor["hate"];

          let tempHtml = `<div id="right-top">${foodCategory} 추천 메뉴</div>
          <div id="card">
              <p id="foodname">${foodName}</p>
              <p id="storename">${shopName}</p>
              <p id="address">주소 : ${shopAddress}</p>
              <img src="${shopImg}">
              <div class="field is-grouped">
                  <p class="control">
                      <input type="checkbox" name="category" id="좋아요">좋아요
                  </p>
                  <p class="control">
                      <input type="checkbox" name="category" id="싫어요">싫어요
                  </p>
              </div>
              <p>좋아요 : ${like}개</p>
              <p>싫어요 : ${hate}개</p>
              <hr>`;
          $("#right").append(tempHtml);
        }
      },
    });
  } else {
    $("#right").empty;
  }
}
function showWest() {
  $("#right").empty();
  let checkWest = $("#양식").is(":checked");
  if (checkWest) {
    $.ajax({
      type: "GET",
      url: "/api/west",
      data: {},
      success: function (response) {
        let wests = response["west_list"];
        for (let i = 0; i < wests.length; i++) {
          let west = wests[i];
          let foodName = west["food_name"];
          let foodCategory = west["food_category"];
          let shopName = west["shop_name"];
          let shopAddress = west["shop_address"];
          let shopImg = west["shop_img"];
          let like = west["like"];
          let hate = west["hate"];

          let tempHtml = `<div id="right-top">${foodCategory} 추천 메뉴</div>
          <div id="card">
              <p id="foodname">${foodName}</p>
              <p id="storename">${shopName}</p>
              <p id="address">주소 : ${shopAddress}</p>
              <img src="${shopImg}">
              <div class="field is-grouped">
                  <p class="control">
                      <input type="checkbox" name="category" id="좋아요">좋아요
                  </p>
                  <p class="control">
                      <input type="checkbox" name="category" id="싫어요">싫어요
                  </p>
              </div>
              <p>좋아요 : ${like}개</p>
              <p>싫어요 : ${hate}개</p>
              <hr>`;
          $("#right").append(tempHtml);
        }
      },
    });
  } else {
    $("#right").empty;
  }
}
function showCn() {
  $("#right").empty();
  let checkCn = $("#중식").is(":checked");
  if (checkCn) {
    $.ajax({
      type: "GET",
      url: "/api/cn",
      data: {},
      success: function (response) {
        let cns = response["cn_list"];
        for (let i = 0; i < cns.length; i++) {
          let cn = cns[i];
          let foodName = cn["food_name"];
          let foodCategory = cn["food_category"];
          let shopName = cn["shop_name"];
          let shopAddress = cn["shop_address"];
          let shopImg = cn["shop_img"];
          let like = cn["like"];
          let hate = cn["hate"];

          let tempHtml = `<div id="right-top">${foodCategory} 추천 메뉴</div>
          <div id="card">
              <p id="foodname">${foodName}</p>
              <p id="storename">${shopName}</p>
              <p id="address">주소 : ${shopAddress}</p>
              <img src="${shopImg}">
              <div class="field is-grouped">
                  <p class="control">
                      <input type="checkbox" name="category" id="좋아요">좋아요
                  </p>
                  <p class="control">
                      <input type="checkbox" name="category" id="싫어요">싫어요
                  </p>
              </div>
              <p>좋아요 : ${like}개</p>
              <p>싫어요 : ${hate}개</p>
              <hr>`;
          $("#right").append(tempHtml);
        }
      },
    });
  } else {
    $("#right").empty();
  }
}
function showJp() {
  $("#right").empty();
  let checkJp = $("#일식").is(":checked");
  if (checkJp) {
    $.ajax({
      type: "GET",
      url: "/api/jp",
      data: {},
      success: function (response) {
        let jps = response["jp_list"];
        for (let i = 0; i < jps.length; i++) {
          let jp = jps[i];
          let foodName = jp["food_name"];
          let foodCategory = jp["food_category"];
          let shopName = jp["shop_name"];
          let shopAddress = jp["shop_address"];
          let shopImg = jp["shop_img"];
          let like = jp["like"];
          let hate = jp["hate"];

          let tempHtml =`<div id="right-top">${foodCategory} 추천 메뉴</div>
          <div id="card">
              <p id="foodname">${foodName}</p>
              <p id="storename">${shopName}</p>
              <p id="address">주소 : ${shopAddress}</p>
              <img src="${shopImg}">
              <div class="field is-grouped">
                  <p class="control">
                      <input type="checkbox" name="category" id="좋아요">좋아요
                  </p>
                  <p class="control">
                      <input type="checkbox" name="category" id="싫어요">싫어요
                  </p>
              </div>
              <p>좋아요 : ${like}개</p>
              <p>싫어요 : ${hate}개</p>
              <hr>`;
          $("#right").append(tempHtml);
        }
      },
    });
  } else {
    $("#right").empty;
  }
}
function showEtc() {
  $("#right").empty();
  let checkKEtc = $("#기타").is(":checked");
  if (checkKEtc) {
    $.ajax({
      type: "GET",
      url: "/api/etc",
      data: {},
      success: function (response) {
        let etcs = response["etc_list"];
        for (let i = 0; i < etcs.length; i++) {
          let etc = etcs[i];
          let foodName = etc["food_name"];
          let foodCategory = etc["food_category"];
          let shopName = etc["shop_name"];
          let shopAddress = etc["shop_address"];
          let shopImg = etc["shop_img"];
          let like = etc["like"];
          let hate = etc["hate"];

          let tempHtml = `<div id="right-top">${foodCategory} 추천 메뉴</div>
          <div id="card">
              <p id="foodname">${foodName}</p>
              <p id="storename">${shopName}</p>
              <p id="address">주소 : ${shopAddress}</p>
              <img src="${shopImg}">
              <div class="field is-grouped">
                  <p class="control">
                      <input type="checkbox" name="category" id="좋아요">좋아요
                  </p>
                  <p class="control">
                      <input type="checkbox" name="category" id="싫어요">싫어요
                  </p>
              </div>
              <p>좋아요 : ${like}개</p>
              <p>싫어요 : ${hate}개</p>
              <hr>`;
          $("#right").append(tempHtml);
        }
      },
    });
  } else {
    $("#right").empty;
  }
  function like(name) {
    $.ajax({
      type: 'POST',
      url: '/api/like',
      data: {'name_give': name},
      success: function(response) {
        if (response['result'] == 'success') {
          alert('좋아요 완료!');
        }
        window.location.reload();
      }
    });
  }
}
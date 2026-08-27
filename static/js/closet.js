function register() {
  let brand = $("#brand").val();
  let name = $("#name").val();
  let fileInput = $("#clothpic")[0];
  let file = fileInput.files[0];
  let buydate = $("#buydate").val();
  let buymethod = $("#buymethod").val();
  let price = $("#price").val();
  let season = $("#season").val();
  let clothtype = $("#clothtype").val();
  let clothsize = $("#clothsize").val();

  // 예외 처리
  if (!file) {
    alert("옷 사진을 선택해 주세요.");
    return;
  }

  let formData = new FormData();
  formData.append("file", file);
  formData.append("name", name);
  formData.append("brand", brand);
  formData.append("date", buydate);
  formData.append("method", buymethod);
  formData.append("price", price);
  formData.append("season", season);
  formData.append("type", clothtype);
  formData.append("size", clothsize);

  $.ajax({
    type: "POST",
    url: "/closet/register",
    data: formData,
    processData: false, //파일 전송 시 필수 설정
    contentType: false, //파일 전송 시 필수 설정
    success: function (response) {
      alert("등록되었습니다.");
      window.location.href = "/closet";
    },
  });
}

document.querySelector("#clothtype").addEventListener("change", function () {
    const size = document.querySelector("#clothsize");

    if (this.value === "신발") {
      size.innerHTML = `
            <option value="220">220</option>
            <option value="225">225</option>
            <option value="230">230</option>
            <option value="235">235</option>
            <option value="240">240</option>
            <option value="245">245</option>
            <option value="250">250</option>
            <option value="255">255</option>
            <option value="260">260</option>
            <option value="265">265</option>
            <option value="270">270</option>
            <option value="275">275</option>
            <option value="280">280</option>
            <option value="285">285</option>
            <option value="290">290</option>
            <option value="295">295</option>
            <option value="300">300</option>
        `;
    } else {
      size.innerHTML = `
            <option value="FREE">FREE</option>
            <option value="XS">XS</option>
            <option value="S">S</option>
            <option value="M">M</option>
            <option value="L">L</option>
            <option value="XL">XL</option>
            <option value="XXL">XXL</option>
        `;
    }
  });
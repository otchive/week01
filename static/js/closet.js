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
        }
    });
}

function proceedLogin() {
    let id = $("#input-id").val();
    let pw = $("#input-pw").val();

    $.ajax({
        method: "POST",
        url: `/auth/login`,
        data: { "userid": id, "userpw": pw },
        success: function (response) {
            alert(response["message"]);

            if (response["status"] == "success") {
                window.location.href = "/";
            }
        }
    });
}

function proceedLogout() {
    $.ajax({
        method: "GET",
        url: "/auth/logout",
        data: {},
        success: function(response) {
            alert("로그아웃 되었습니다.");
            window.location.href = "/";
        }
    });
}

function checkIDisUnique() {
    let ID = $("#id-input").val();
    console.log(ID);
    $.ajax({
        method: "GET",
        url: `/auth/check-id?id=${ID}`,
        data: {},
        success: function (response) {
            alert(response["message"]);

            if (response["status"] == "success") {
                $("#check-id-unique").attr("disabled", true);
            }
        }
    });
}

function checkNickisUnique() {
    let nick = $("#nick-input").val();
    console.log(nick);
    $.ajax({
        method: "GET",
        url: `/auth/check-nickname?nick=${nick}`,
        data: {},
        success: function (response) {
            alert(response["message"]);

            if (response["status"] == "success") {
                $("#check-nick-unique").attr("disabled", true);
            }
        }
    });
}

function proceedSignup() {
    let idChecked = $("#check-id-unique").prop("disabled");
    let nickChecked = $("#check-nick-unique").prop("disabled");

    let id = $("#id-input").val();
    let pw = $("#pw-input").val();
    let nick = $("#nick-input").val();
    let pwcheck = $("#pw-input-check").val();

    if (idChecked || nickChecked == false) {
        if (pw != pwcheck) {
            alert("비밀번호 확인란이 일치하는지 다시 확인해주세요.");
        }

        else {
            $.ajax({
                method: "POST",
                url: "/auth/signup",
                data: { "final_id": id, "final_pw": pw, "final_nick": nick },
                success: function (response) {
                    alert(response["message"]);
                    window.location.href = '/';
                }
            });
        }
    }
}

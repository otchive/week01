function toggleEditMode(isEdit) {
  const viewElements = document.querySelectorAll(".view-mode");
  const editElements = document.querySelectorAll(".edit-mode");

  viewElements.forEach((el) => el.classList.toggle("is-hidden", isEdit));
  editElements.forEach((el) => el.classList.toggle("is-hidden", !isEdit));
}

function saveChanges(itemId) {
  const form = document.getElementById("detail-form");
  const formData = new FormData(form);

  fetch(`/closet/${itemId}/edit`, {
    method: "POST",
    body: formData,
  })
    .then((res) => res.json())
    .then((data) => {
      alert("수정되었습니다.");
      location.reload();
    });
}

function deleteItem(itemId) {
    if (!confirm("정말 삭제하시겠습니까?")) {
        return;
    }

    $.ajax({
        type: "DELETE",
        url: `/closet/${itemId}/delete`,
        success: function (response) {
            alert("삭제되었습니다.");
            window.location.href = "/closet";
        },
        error: function (xhr) {
            alert(xhr.responseJSON?.message || "삭제에 실패했습니다.");
        },
    });
}

function toggleLifeFit(itemId) {
    $.ajax({
        type: "POST",
        url: `/closet/${itemId}/life-fit`,

        success: function (response) {
            alert("변경되었습니다.");
            location.reload();
        },
        error: function (xhr) {
            alert(xhr.responseJSON?.message || "등록에 실패했습니다.");
        },
    });
}

function wearItem(itemId) {
    $.ajax({
        type: "POST",
        url: `/closet/${itemId}/wear`,

        success: function (response) {
            $("wear-count").text(
                `착용횟수: ${response.wear_count}회`
            );

            alert(response.message);
            location.reload();
        },

        error: function (xhr) {
            alert(xhr.responseJSON?.message || "업데이트에 실패했습니다.");
        },
    });
}
export function displayMemberDetail(data) {
  // 主會員介面的顯示
  const name = document.querySelector(".user-name");
  name.textContent = escapeHtml(data.name);
  const accountId = document.querySelector(".user-account-id");
  accountId.textContent = "@ " + escapeHtml(data.account_id);
  const self_intro = document.querySelector(".user-self-intro");
  self_intro.textContent = escapeHtml(data.self_intro);
  const fans_counts = document.querySelector(".user-fans");
  fans_counts.textContent = data.fans_counts + " 位粉絲";

  // 頭像判斷
  const avatarUrl = data.avatar;
  const profileAvatar = document.querySelector(".profile-avatar");
  profileAvatar.innerHTML = "";

  if (data.avatar !== null) {
    const img = document.createElement("img");
    img.src = avatarUrl;
    img.alt = "User Avatar";
    img.classList.add("profile-pic");
    profileAvatar.append(img);
  } else {
    const icon = document.createElement("i");
    icon.classList.add("fa-regular", "fa-circle-user", "profile-pic");
    profileAvatar.append(icon);
  }

  // 編輯會員介面的顯示
  const editName = document.querySelector("#username");
  editName.placeholder = escapeHtml(data.name);
  const editSelf = document.querySelector("#bio");
  editSelf.placeholder =
    data.self_intro === null ? "" : escapeHtml(data.self_intro);

  const editAvatar = document.querySelector(".edit-profile-avatar");
  console.log("editAvatar:", editAvatar);

  if (data.avatar === null) {
    const icon = document.createElement("i");
    icon.classList.add(
      "fa-regular",
      "fa-circle-user",
      "profile-pic",
      "edit-profile-pic"
    );
    editAvatar.append(icon);
  } else {
    const editImg = document.createElement("img");
    editImg.src = data.avatar;
    editImg.classList.add("profile-pic", "edit-profile-pic");
    editAvatar.append(editImg);
  }
}

function escapeHtml(unsafe) {
  return unsafe
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

export function closeEditMember() {
  const editProfile = document.querySelector(".edit-profile-modal");
  const postForm = document.querySelector(".edit-profile-form");
  // 點擊遮罩地方可以關閉
  editProfile.addEventListener("click", function (event) {
    if (event.target === editProfile) {
      closeModal();
    }
  });

  // 關閉
  function closeModal() {
    editProfile.style.display = "none";
    postForm.reset();
  }
}

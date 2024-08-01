import {
  fetchMemberDetail,
  fetchGetPost,
  validateForm,
} from "./controller/controller_member.js";
import { closeEditMember } from "./view/view_member.js";
import { PermissionAllIcon } from "./view/view_icon.js";

document.addEventListener("DOMContentLoaded", async function () {
  PermissionAllIcon();
  closeEditMember();
  fetchMemberDetail();
  await fetchGetPost();

  uploadAvatar();

  const OutsideMemberBtn = document.querySelector(".edit-profile-button");
  OutsideMemberBtn.addEventListener("click", editMember);
});

function editMember(event) {
  event.preventDefault();
  const displayEditMember = document.querySelector(".edit-profile-modal");
  displayEditMember.style.display = "flex";
  // 提交更新會員按鈕
  const submitUpdateMember = document.querySelector(".save-button");
  submitUpdateMember.addEventListener("click", function (event) {
    event.preventDefault();
    validateForm();
  });
}

function uploadAvatar() {
  const avatarIcon = document.querySelector(
    ".edit-profile-avatar i.profile-pic"
  );
  const avatarUploadInput = document.getElementById("avatar-upload-input");

  // 點擊該頭像
  avatarIcon.addEventListener("click", function () {
    avatarUploadInput.click();
  });

  // 頭像事件
  avatarUploadInput.addEventListener("change", function () {
    const file = this.files[0];
    console.log("file:", file);
    if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
        // 隱藏圖標
        avatarIcon.style.display = "none";

        // 預覽圖片
        let img = document.getElementById("avatar-preview");
        if (!img) {
          img = document.createElement("img");
          img.id = "avatar-preview";
          const avatarContainer = document.querySelector(
            ".edit-profile-avatar"
          );
          avatarContainer.appendChild(img);
        }
        img.src = e.target.result;

        // 樣式
        img.style.width = "80px";
        img.style.height = "80px";
        img.style.borderRadius = "50%";
        img.style.objectFit = "cover";
        img.style.position = "absolute";
        img.style.top = "50%";
        img.style.left = "50%";
        img.style.transform = "translate(-50%, -50%)";
      };
      reader.readAsDataURL(file);
      // avatarUploadInput.value = "";
    }
  });
}

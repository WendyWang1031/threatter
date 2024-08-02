import { displayMemberDetail } from "../view/view_member.js";

import { uploadMediaFile } from "./controller_upload.js";

export function editMember(event) {
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

export function uploadAvatar() {
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

export async function fetchMemberDetail() {
  const account_id = localStorage.getItem("account_id");
  const memberUrl = `/api/member/${encodeURIComponent(account_id)}`;
  if (!account_id) {
    console.log("User not logged in, using default avatar.");
    return;
  }
  try {
    const response = await fetch(memberUrl);
    const result = await response.json();

    if (result) {
      displayMemberDetail(result);
    } else {
      console.error("Failed to retrieve post data.");
    }
  } catch (error) {
    console.error("Error fetching post data:", error);
  }
}

export function validateForm() {
  const error_hint = document.querySelector(".error-message");
  const form = document.querySelector(".edit-profile-form");
  const content = form.querySelector("textarea").value.trim();

  const userName_input = document.getElementById("username").value;
  console.log("userName_input:", userName_input);

  const imageUploadInput = document.getElementById("avatar-upload-input");
  console.log("imageUploadInput:", imageUploadInput);

  let imageFile = null;
  if (imageUploadInput && imageUploadInput.files) {
    imageFile = imageUploadInput.files[0] || null;
  }

  console.log("imageFile:", imageFile);

  if (content === "" && !imageFile && !userName_input) {
    error_hint.textContent = "請至少更新一個欄位";
    return false;
  }
  submitPost(content, imageFile, userName_input);
  return true;
}

async function submitPost(content, imageFile, userName) {
  let memberData = {
    name: userName || "",
    visibility: "public",
    self_intro: content || "",
    avatar: "",
  };
  console.log("memberData:", memberData);

  // 圖片
  if (imageFile) {
    const imageUrl = await uploadMediaFile(imageFile);
    if (imageUrl) {
      memberData.avatar = imageUrl;
    }
  }

  try {
    await fetchUpdateMember(memberData);
  } catch (error) {
    console.error("Error submitting member:", error);
    alert("Failed to submit member: " + error.message);
  }
}

async function fetchUpdateMember(memberData) {
  const memberUpdateURL = "/api/member";
  const token = localStorage.getItem("userToken");
  console.log("memberData:", JSON.stringify(memberData));

  try {
    const response = await fetch(memberUpdateURL, {
      method: "PATCH",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(memberData),
    });

    if (!response.ok) {
      console.log("Failed to member details:", response.status);

      throw new Error(`HTTP status ${response.status}`);
    } else {
      window.location.reload();
    }
  } catch (error) {
    console.error("Error updating member data", error);
  } finally {
  }
}
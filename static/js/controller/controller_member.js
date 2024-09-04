import { displayMemberDetail } from "../view/view_member.js";

import { uploadMediaFile } from "./controller_upload.js";
import { stringifyObjectValues } from "./controller_convert_to_string.js";

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
    ".edit-profile-avatar",
    ".edit-profile-pic"
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
        // avatarIcon.style.display = "none";

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
  document.getElementById("loading").classList.remove("hidden");
  const followProfileButtonContainer = document.querySelector(
    ".follow-profile-button"
  );

  const userToken = localStorage.getItem("userToken");

  const currentUrl = window.location.pathname;
  const urlAccountId = currentUrl.split("/").pop();

  if (!userToken) {
    // 用戶未登入，隱藏追蹤按鈕
    followProfileButtonContainer.style.display = "none";
  }

  // 抓取當前用戶
  const localAccountId = localStorage.getItem("account_id");

  // 判斷是否當前用戶
  const isCurrentUser = urlAccountId === localAccountId;
  const account_id = isCurrentUser ? localAccountId : urlAccountId;

  if (!account_id) {
    console.log("User not logged in, using default avatar.");
    return;
  }

  // 目前的token是否須攜帶 可選
  const headers = userToken ? { Authorization: `Bearer ${userToken}` } : {};

  try {
    const response = await fetch(
      `/api/member/${encodeURIComponent(account_id)}`,
      {
        headers: headers,
      }
    );
    let result = await response.json();

    if (result) {
      result = stringifyObjectValues(result);

      displayMemberDetail(result);
      // 顯示或隱藏按鈕
      const followProfileButton =
        followProfileButtonContainer.querySelector("button");
      const editProfileButton = document.querySelector(".edit-profile-button");

      if (!userToken) {
        // 用戶未登入，隱藏追蹤按鈕
        followProfileButtonContainer.style.display = "none";
      }

      if (isCurrentUser) {
        // 顯示編輯會員按鈕
        editProfileButton.style.display = "block";
        followProfileButtonContainer.style.display = "none";
      } else {
        // 顯示追蹤按鈕
        editProfileButton.style.display = "none";
        if (userToken) {
          followProfileButtonContainer.style.display = "block";

          // 根據 follow_state 動態設置按鈕文本
          let buttonText;
          switch (result.follow_state) {
            case "None":
              buttonText = "追蹤";
              break;
            case "Following":
              buttonText = "追蹤中";
              break;
            case "Pending":
              buttonText = "請求追蹤中";
              break;
            default:
              buttonText = "追蹤";
          }
          followProfileButton.textContent = buttonText;

          // 添加點擊事件處理程序
          followProfileButtonContainer.addEventListener(
            "click",
            async function () {
              // 保存當前狀態以便回滾
              const previousState = {
                follow_state: result.follow_state,
                buttonText: followProfileButton.textContent,
              };

              // 根據當前狀態決定要傳遞的 follow 值
              let followValue;
              if (result.follow_state === "Following") {
                followValue = false; // 取消追蹤
              } else if (result.follow_state === "None") {
                followValue = true; // 發起追蹤
              } else if (result.follow_state === "Pending") {
                followValue = false; // 取消請求
              }

              // 即時更新按鈕狀態
              followProfileButton.textContent = followValue ? "追蹤中" : "追蹤";

              try {
                const apiEndpoint = "/api/follow";
                const response = await fetch(apiEndpoint, {
                  method: "POST",
                  headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${localStorage.getItem(
                      "userToken"
                    )}`,
                  },
                  body: JSON.stringify({
                    follow: followValue,
                    account_id: result.account_id,
                  }),
                });

                if (response.ok) {
                  const res = await response.json();
                  if (res.follow_state === "Following") {
                    followProfileButton.textContent = "追蹤中";
                    result.follow_state = "Following";
                  } else if (res.follow_state === "Pending") {
                    followProfileButton.textContent = "請求追蹤中";
                    result.follow_state = "Pending";
                  } else {
                    followProfileButton.textContent = "追蹤";
                    result.follow_state = "None";
                  }
                } else {
                  const errorResult = await response.json();
                  console.error("操作失敗:", errorResult);

                  // API 響應失敗時回滾狀態
                  followProfileButton.textContent = previousState.buttonText;
                  result.follow_state = previousState.follow_state;
                }
              } catch (error) {
                console.error("請求錯誤:", error);

                // 請求出錯時回滾狀態
                followProfileButton.textContent = previousState.buttonText;
                result.follow_state = previousState.follow_state;
              }
            }
          );
        }
      }
    } else {
      console.error("Failed to retrieve member data.");
    }
  } catch (error) {
    console.error("Error fetching member data:", error);
  } finally {
    document.getElementById("loading").classList.add("hidden");
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

  const privacyInput = document.getElementById("privacy");
  const visibility = privacyInput.checked ? "Private" : "Public";

  if (content === "" && !imageFile && !userName_input && !visibility) {
    error_hint.textContent = "請至少更新一個欄位";
    return false;
  }
  submitMember(content, imageFile, userName_input, visibility);
  return true;
}

async function submitMember(content, imageFile, userName, visibility) {
  document.getElementById("loading").classList.remove("hidden");

  let memberData = {
    name: userName || "",
    visibility: visibility,
    self_intro: content || "",
    avatar: "",
  };

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
  } finally {
    document.getElementById("loading").classList.add("hidden");
  }
}

async function fetchUpdateMember(memberData) {
  const memberUpdateURL = "/api/member";
  const token = localStorage.getItem("userToken");

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

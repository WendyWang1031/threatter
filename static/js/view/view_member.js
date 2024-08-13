export function displayMemberDetail(data) {
  // 主會員介面的顯示
  const name = document.querySelector(".user-name");
  name.textContent = data.name;
  const accountId = document.querySelector(".user-account-id");
  accountId.textContent = "@ " + data.account_id;
  const self_intro = document.querySelector(".user-self-intro");
  self_intro.textContent = data.self_intro;
  const fans_counts = document.querySelector(".user-fans");
  fans_counts.textContent = data.fans_counts + " 位粉絲";

  // 頭像判斷
  const avatarUrl = data.avatar;
  if (avatarUrl) {
    const img = document.createElement("img");
    img.src = avatarUrl;
    img.alt = "User Avatar";
    img.classList.add("profile-pic");
  } else {
    const icon = document.createElement("i");
    icon.classList.add("fa-regular", "fa-circle-user", "profile-pic");
  }

  // 編輯會員介面的顯示
  const editName = document.querySelector("#username");
  editName.placeholder = data.name;
  const editSelf = document.querySelector("#bio");
  editSelf.placeholder = data.self_intro;

  const editAvatar = document.querySelector(".profile-pic");
  const editImg = document.createElement("img");
  editImg.src = data.avatar;
  editImg.classList.add("profile-pic");
  editAvatar.replaceWith(editImg);
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

export function displayOrCloseFansAndFollow() {
  const fans_follow_container = document.querySelector(".fans-follow");
  fans_follow_container.style.display = "flex";

  // 點擊遮罩地方可以關閉
  fans_follow_container.addEventListener("click", function (event) {
    if (event.target === fans_follow_container) {
      closeModal();
    }
  });

  // 關閉
  function closeModal() {
    fans_follow_container.style.display = "none";
  }
}

export function setupTabSwitching() {
  const tabs = document.querySelectorAll(".follower-header .tab");
  const lists = document.querySelectorAll(".follower-list");

  tabs.forEach((tab) => {
    tab.addEventListener("click", function () {
      // 移除所有標籤的 active
      tabs.forEach((t) => t.classList.remove("active"));
      // 添加 active
      this.classList.add("active");

      // 隱藏
      lists.forEach((list) => (list.style.display = "none"));

      const targetListClass = this.getAttribute("data-target");
      document.querySelector(`.${targetListClass}`).style.display = "block";
    });
  });
}

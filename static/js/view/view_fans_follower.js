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

export function displayFollowerItem(data) {
  const item = document.createElement("div");
  item.className = "list-item";
  console.log("data:", data);

  // 生成頭像的 HTML
  let avatarHtml;
  if (data.user.avatar) {
    avatarHtml = `<img src="${data.user.avatar}" alt="${data.user.account_id}'s avatar" class="profile-pic">`;
  } else {
    avatarHtml = `<i class="fa-regular fa-circle-user profile-pic"></i>`;
  }

  item.innerHTML = `
      ${avatarHtml}
        <div class="list-user-info">
          <a href="/api/member/${encodeURIComponent(
            data.user.account_id
          )}" class="list-username">${data.user.account_id}</a>
          <div class="list-user-fullname">${data.user.name}</div>
        </div>
        <button class="list-follow-btn">${
          data.follow_state ? "取消追蹤" : "追蹤"
        }</button>
      `;

  return item;
}

export function displayFollowerItem(data) {
  const item = document.createElement("div");
  item.className = "list-item";

  // 生成頭像
  let avatarHtml;
  if (data.user.avatar) {
    avatarHtml = `<img src="${data.user.avatar}" alt="${data.user.account_id}'s avatar" class="profile-pic">`;
  } else {
    avatarHtml = `<i class="fa-regular fa-circle-user profile-pic"></i>`;
  }

  item.innerHTML = `
        ${avatarHtml}
          <div class="list-user-info">
            <a href="/member/${encodeURIComponent(
              data.user.account_id
            )}" class="list-username">${data.user.account_id}</a>
            <div class="list-user-fullname">${data.user.name}</div>
          </div>
        `;

  // 接受和拒絕的按鈕
  const actionButtons = document.createElement("div");
  actionButtons.className = "action-buttons";

  const acceptBtn = document.createElement("button");
  acceptBtn.className = "accept-btn";
  acceptBtn.textContent = "接受";
  acceptBtn.addEventListener("click", async function () {
    try {
      const response = await fetch("/api/follow/accept", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("userToken")}`,
        },
        body: JSON.stringify({ account_id: data.user.account_id }),
      });

      if (response.ok) {
        console.log("接受成功");
        item.style.display = "none"; // 移除列表项
      } else {
        console.error("接受失敗");
      }
    } catch (error) {
      console.error("請求失敗:", error);
    }
  });

  const rejectBtn = document.createElement("button");
  rejectBtn.className = "reject-btn";
  rejectBtn.textContent = "拒絕";
  rejectBtn.addEventListener("click", async function () {
    try {
      const response = await fetch("/api/follow/reject", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("userToken")}`,
        },
        body: JSON.stringify({ account_id: data.user.account_id }),
      });

      if (response.ok) {
        console.log("拒絕成功");
        item.style.display = "none"; // 移除列表项
      } else {
        console.error("拒絕失敗");
      }
    } catch (error) {
      console.error("請求失敗:", error);
    }
  });

  actionButtons.appendChild(acceptBtn);
  actionButtons.appendChild(rejectBtn);

  item.appendChild(actionButtons);
  return item;
}

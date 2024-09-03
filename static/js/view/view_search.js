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

  let account_id = data.user.account_id;
  account_id = escapeHtml(account_id);

  let name = data.user.name;
  name = escapeHtml(name);

  item.innerHTML = `
        ${avatarHtml}
          <div class="list-user-info">
            <a href="/member/${encodeURIComponent(
              account_id
            )}" class="list-username">${account_id}</a>
            <div class="list-user-fullname">${name}</div>
            
          </div>
        `;

  const currentAccountId = localStorage.getItem("account_id");

  // 如果是自己帳號，不顯示追蹤按鈕
  if (data.user.account_id === currentAccountId) {
    return item;
  }

  let buttonText;

  switch (data.follow_state) {
    case "None":
      buttonText = "追蹤";
      break;
    case "Following":
      buttonText = "追蹤中";
      break;
    case "Pending":
      buttonText = "取消請求";
      break;
    default:
      buttonText = "追蹤";
  }
  // 生成按鈕對應相對應的追蹤 api

  const button = document.createElement("button");
  button.className = "list-follow-btn";
  button.textContent = buttonText;
  button.style.display = "block";

  const updateButtonState = (followState) => {
    if (followState === "Following") {
      button.textContent = "追蹤中";
      button.style.display = "block";
    } else if (followState === "Pending") {
      button.textContent = "請求追蹤中";
      button.style.display = "block";
    } else {
      button.textContent = "追蹤";
      button.style.display = "block";
    }
    button.style.display = "block";
  };

  button.addEventListener("click", async function () {
    try {
      // 保存當前狀態，以便在失敗時回滾
      const previousState = {
        follow_state: data.follow_state,
        buttonText: button.textContent,
      };

      // 根據當前的 follow_state 決定 follow 的狀態
      const followAction =
        data.follow_state === "None" || data.follow_state === "BeingFollow";

      // 即時更新按鈕狀態
      if (followAction) {
        button.textContent = "追蹤中";
        data.follow_state = "Following";
      } else {
        button.textContent = "追蹤";
        data.follow_state = "None";
      }

      const response = await fetch("/api/follow", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("userToken")}`,
        },
        body: JSON.stringify({
          follow: followAction,
          account_id: data.user.account_id,
        }),
      });

      if (response.ok) {
        const result = await response.json();
        console.log("操作成功:", result);

        // 更新按鈕狀態根據返回的 follow_state
        if (result.follow_state === "Following") {
          button.textContent = "追蹤中";
          data.follow_state = "Following";
        } else if (result.follow_state === "Pending") {
          button.textContent = "請求追蹤中";
          data.follow_state = "Pending";
        } else {
          button.textContent = "追蹤";
          data.follow_state = "None";
        }
      } else {
        const errorResult = await response.json();
        console.error("操作失敗:", errorResult);

        // 如果 API 響應失敗，回滾按鈕狀態
        button.textContent = previousState.buttonText;
        data.follow_state = previousState.follow_state;
      }
    } catch (error) {
      console.error("請求錯誤:", error);

      // 如果請求出錯，回滾按鈕狀態
      button.textContent = previousState.buttonText;
      data.follow_state = previousState.follow_state;
    }
  });

  item.appendChild(button);

  return item;
}

function escapeHtml(text) {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

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
  button.style.display = "none";

  const actionButtons = document.createElement("div");
  actionButtons.className = "action-buttons";

  const acceptBtn = document.createElement("button");
  acceptBtn.className = "accept-btn";
  acceptBtn.textContent = "接受";

  const rejectBtn = document.createElement("button");
  rejectBtn.className = "reject-btn";
  rejectBtn.textContent = "拒絕";

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
    rejectBtn.style.display = "none";
    acceptBtn.style.display = "none";
  };

  acceptBtn.addEventListener("click", async function () {
    try {
      const response = await fetch("/api/follow/member/follow", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("userToken")}`,
        },
        body: JSON.stringify({
          accept: true,
          account_id: data.user.account_id,
        }),
      });

      if (response.ok) {
        const result = await response.json();
        console.log("接受追蹤成功:", result);
        updateButtonState(result.follow_state);
      } else {
        console.error("接受失敗");
      }
    } catch (error) {
      console.error("請求失敗:", error);
    }
  });

  rejectBtn.addEventListener("click", async function () {
    try {
      const response = await fetch("/api/follow/member/follow", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("userToken")}`,
        },
        body: JSON.stringify({
          accept: false,
          account_id: data.user.account_id,
        }),
      });

      if (response.ok) {
        const result = await response.json();
        console.log("拒絕追蹤成功:", result);
        updateButtonState(result.follow_state);
      } else {
        console.error("拒絕失敗");
      }
    } catch (error) {
      console.error("請求失敗:", error);
    }
  });

  button.addEventListener("click", async function () {
    try {
      // 保存當前狀態，以便在失敗時回滾
      const previousState = {
        follow_state: data.follow_state,
        buttonText: button.textContent,
      };

      // 根據當前的 follow_state 決定 follow 的狀態
      const followAction = data.user.follow_state !== "Following";
      // 即時更新按鈕狀態
      button.textContent = followAction ? "追蹤中" : "追蹤";
      data.user.follow_state = followAction ? "Following" : "None";

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

  actionButtons.appendChild(acceptBtn);
  actionButtons.appendChild(rejectBtn);

  item.appendChild(actionButtons);
  item.appendChild(button);

  return item;
}

export function displayNotificationItem(data) {
  const item = document.createElement("div");
  item.className = `list-item ${data.event_type.toLowerCase()} indivisual-list`;

  // 生成頭像
  let avatarHtml;
  if (data.user.user.avatar) {
    avatarHtml = `<img src="${data.user.user.avatar}" alt="${data.user.user.account_id}'s avatar" class="profile-pic">`;
  } else {
    avatarHtml = `<i class="fa-regular fa-circle-user profile-pic"></i>`;
  }

  item.innerHTML = `
        <div class="header-area">
          ${avatarHtml}
          <div class="list-user-info">
            <a href="/member/${encodeURIComponent(
              data.user.user.account_id
            )}" class="list-username">${data.user.user.account_id}</a>
            <div class="list-user-fullname">${data.user.user.name}</div>
          </div>
          <div class="hint_area">${getHintAreaContent(data)}</div>
          <div class="created_at">${formatTimeToTaipeiTime(
            data.created_at
          )}</div>
        </div>
        ${getContentArea(data)}
      `;

  // 生成追蹤按鈕
  const followButton = generateFollowButton(data);
  if (followButton) {
    const headerArea = item.querySelector(".header-area");
    const hintArea = item.querySelector(".hint_area");
    headerArea.insertBefore(followButton, hintArea);
  }

  return item;
}

// 根據 event_type 生成提示文字
function getHintAreaContent(data) {
  switch (data.event_type) {
    case "Follow":
      return `追蹤 <i class="fa-solid fa-user-plus"></i>`;
    case "Like":
      return `按讚 <i class="fa-solid fa-heart"></i>`;
    case "Reply":
      return `回覆 <i class="fa-solid fa-reply"></i>`;
    default:
      return "";
  }
}

// 根據 event_type 生成內容區域
function getContentArea(data) {
  let parentText = data.event_data.parent?.text || "";
  if (!parentText) {
    if (data.event_data.parent?.media?.images) {
      parentText = "[圖片內容]";
    } else if (data.event_data.parent?.media?.videos) {
      parentText = "[影片內容]";
    } else if (data.event_data.parent?.media?.audios) {
      parentText = "[音訊內容]";
    } else {
      parentText = "[多媒體內容]";
    }
  }

  if (data.event_type === "Follow") {
    let followText = "";
    switch (data.event_data.status) {
      case "Pending":
        followText = "提出要求追蹤";
        break;
      case "Following":
        followText = "已追蹤您";
        break;
      case "Accepted":
        followText = "已接受您的追蹤請求";
        break;
      default:
        followText = "已追蹤您";
    }
    return `
    <div class="content_area">
      <div class="content">${followText}</div>
    </div>
      `;
  } else if (data.event_type === "Like" || data.event_type === "Reply") {
    return `
      <div class="content_area">
        <div class="content">${parentText}</div>
        ${
          data.event_type === "Reply"
            ? `<div class="reply">${data.event_data.children?.text || ""}</div>`
            : ""
        }
        <a href="${data.event_data.parent?.post_url || ""}">前往串文</a>
      </div>
    `;
  }
  return "";
}

// 生成追蹤按鈕並添加事件監聽器
function generateFollowButton(data) {
  // 如果狀態是 "Pending"，不生成按鈕
  if (data.event_data.status === "Pending") {
    return null;
  }

  let buttonText;

  switch (data.user.follow_state) {
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

  if (data.event_type === "Follow") {
    const button = document.createElement("button");
    button.className = "list-follow-btn";
    button.textContent = buttonText;

    button.addEventListener("click", async function () {
      try {
        const followAction =
          data.user.follow_state === "None" ||
          data.user.follow_state === "BeingFollow";

        // 即時更新按鈕狀態
        if (followAction) {
          button.textContent = "追蹤中";
          data.user.follow_state = "Following";
        } else {
          button.textContent = "追蹤";
          data.user.follow_state = "None";
        }

        const response = await fetch("/api/follow", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("userToken")}`,
          },
          body: JSON.stringify({
            follow: followAction,
            account_id: data.user.user.account_id,
          }),
        });

        if (response.ok) {
          const result = await response.json();
          console.log("操作成功:", result);

          if (result.follow_state === "Following") {
            button.textContent = "追蹤中";
          } else if (result.follow_state === "Pending") {
            button.textContent = "請求追蹤中";
          } else {
            button.textContent = "追蹤";
          }
        } else {
          console.error("操作失敗:", await response.json());
          button.textContent = followAction ? "追蹤" : "追蹤中";
        }
      } catch (error) {
        console.error("請求錯誤:", error);
        button.textContent = followAction ? "追蹤" : "追蹤中";
      }
    });

    return button;
  }

  return null;
}

// 格式化時間

function formatTimeToTaipeiTime(utcTime) {
  // 將時間轉乘Date對象
  const createdAtDate = new Date(utcTime + "Z");

  // 換成台北時間
  const taipeiOffset = 8 * 60; // 台北時間時間差
  const taipeiTime = new Date(
    createdAtDate.getTime() + taipeiOffset * 60 * 1000
  );

  // 計算差異
  const now = new Date();
  const diffInMs = now - taipeiTime;
  const diffInSeconds = Math.floor(diffInMs / 1000);
  const diffInMinutes = Math.floor(diffInSeconds / 60);
  const diffInHours = Math.floor(diffInMinutes / 60);
  const diffInDays = Math.floor(diffInHours / 24);

  if (diffInSeconds < 60) {
    return "剛剛";
  } else if (diffInMinutes < 60) {
    return `${diffInMinutes} 分鐘前`;
  } else if (diffInHours < 24) {
    return `${diffInHours} 小時前`;
  } else if (diffInDays < 7) {
    return `${diffInDays} 天前`;
  } else {
    // 超過七天
    return taipeiTime.toLocaleDateString("zh-TW", {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
    });
  }
}

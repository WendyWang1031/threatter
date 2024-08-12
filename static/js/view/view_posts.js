export function displayContentElement(post) {
  // 預設文字
  let defaultText = "";
  // 創建容器
  const indivisial_postElement = document.createElement("div");
  indivisial_postElement.className = "indivisial-area";
  const postElement = document.createElement("div");
  postElement.className = "post";

  // 用戶資料
  const user = post.user || {};
  const account_id = user.account_id;
  const avatar = user.avatar;

  // 生成頭像的 HTML
  let avatarHtml;
  if (avatar) {
    avatarHtml = `<img src="${avatar}" alt="${account_id}'s avatar" class="profile-pic">`;
  } else {
    avatarHtml = `<i class="fa-regular fa-circle-user profile-pic"></i>`;
  }

  // 文字內容
  const textContent =
    post.content && post.content.text
      ? post.content.text.replace(/\n/g, "<br>")
      : "";

  // 媒體內容
  let mediaHtml = "";
  const media = post.content.media || {};
  // console.log("media:", media);

  // 根據媒體類型決定如何顯示
  // 圖片
  if (media.images) {
    mediaHtml += `<img src="${media.images}" alt="Post Image" />`;
  }

  // 影片
  if (media.videos) {
    mediaHtml += `<video controls>
                      <source src="${media.videos}" type="video/mp4">
                      Your browser does not support the video tag.
                    </video>`;
  }

  // 音軌
  if (media.audios) {
    mediaHtml += `<audio controls>
                      <source src="${media.audios}" type="audio/mpeg">
                      Your browser does not support the audio element.
                    </audio>`;
  }

  postElement.innerHTML = `
            <div class="post-header">
              <div class="user-info-post">
              ${avatarHtml}
              <a href="/member/${encodeURIComponent(
                account_id
              )}" class="account_id">${account_id}</a> 
              <div class="created_at">${formatTimeToTaipeiTime(
                post.created_at
              )}</div>
              </div>
              <div class="menu-button">
              <i class="fa fa-ellipsis-h"></i>
              <ul class="dropdown-menu">
                <li class="menu-item delete-post" id="delete-post">刪除</li>
                <li class="menu-item copy-link" id="copy-link">複製連結</li>
              </ul>
              </div>
            </div>
            <div class="post-content">
              <div class="post_id" style="display: none">${post.post_id}</div>
              <div class="text">${textContent}</div>
              <div class="media">${mediaHtml}</div>
            </div>
            <div class="post-stats">
            <div class="stat"><i class="fa fa-heart"></i> <span>${
              post.counts.like_counts || 0
            }</span></div>
            <div class="stat"><i class="fa fa-comment"></i> <span>${
              post.counts.reply_counts || 0
            }</span></div>
            <div class="stat"><i class="fa fa-share"></i> <span>${
              post.counts.forward_counts || 0
            }</span></div>
            </div>`;

  indivisial_postElement.appendChild(postElement);
  return indivisial_postElement;
}

export function displayCommentElement(comment) {
  const user = comment.comment.user || {};
  const account_id = user.account_id;
  const avatar = user.avatar;

  const content = comment.comment.content || {};
  const text = content.text || "";
  const media = content.media || {};

  const counts = comment.comment.counts || {};
  const replies = comment.replies || [];

  // 生成頭像的 HTML
  const avatarHtml = avatar
    ? `<img src="${avatar}" alt="${account_id}'s avatar" class="profile-pic">`
    : `<i class="fa-regular fa-circle-user profile-pic"></i>`;

  const textContent = text.replace(/\n/g, "<br>");

  // 媒體內容
  let mediaHtml = "";
  if (media?.images)
    mediaHtml += `<img src="${media.images}" alt="Post Image" />`;
  if (media?.videos)
    mediaHtml += `<video controls><source src="${media.videos}" type="video/mp4">Your browser does not support the video tag.</video>`;
  if (media?.audios)
    mediaHtml += `<audio controls><source src="${media.audios}" type="audio/mpeg">Your browser does not support the audio element.</audio>`;

  const postElement = document.createElement("div");
  postElement.className = "post message";
  postElement.innerHTML = `
    <div class="post-header">
      <div class="user-info-post">
        ${avatarHtml}
        <a href="/member/${encodeURIComponent(
          account_id
        )}" class="account_id">${account_id}</a>
      </div>
      <div class="created_at">${formatTimeToTaipeiTime(post.created_at)}</div>
      <div class="menu-button">
        <i class="fa fa-ellipsis-h"></i>
        <ul class="dropdown-menu">
          <li class="menu-item delete-post" id="delete-post">刪除</li>
          <li class="menu-item copy-link" id="copy-link">複製連結</li>
        </ul>
      </div>
    </div>
    <div class="post-content message-content">
      <div class="post_id message_id" style="display: none">${
        comment.comment.comment_id
      }</div>
      <div class="text">${textContent}</div>
      <div class="media">${mediaHtml}</div>
    </div>
    <div class="post-stats">
      <div class="stat"><i class="fa fa-heart"></i> <span>${
        counts.like_counts || 0
      }</span></div>
      <div class="stat"><i class="fa fa-comment"></i> <span>${
        counts.reply_counts || 0
      }</span></div>
      <div class="stat"><i class="fa fa-share"></i> <span>${
        counts.forward_counts || 0
      }</span></div>
    </div>`;

  replies.forEach((reply) => {
    const replyElement = createReplyElement(reply);
    postElement.appendChild(replyElement);
  });

  const indivisial_postElement = document.createElement("div");
  indivisial_postElement.className = "indivisial-area Comment-Container";
  indivisial_postElement.appendChild(postElement);

  return indivisial_postElement;
}

function createReplyElement(reply) {
  const replyElement = document.createElement("div");
  replyElement.className = "reply-area";

  const user = reply.user || {};
  const account_id = user.account_id;
  const avatar = user.avatar;

  // 生成頭像的 HTML
  let avatarHtml;
  if (avatar) {
    avatarHtml = `<img src="${avatar}" alt="${account_id}'s avatar" class="profile-pic reply-pic">`;
  } else {
    avatarHtml = `<i class="fa-regular fa-circle-user profile-pic reply-pic"></i>`;
  }

  // 文字內容
  const textContent =
    reply.content && reply.content.text
      ? reply.content.text.replace(/\n/g, "<br>")
      : "";

  replyElement.innerHTML = `
            <div class="reply-area-header">
              <div class="user-info-reply">
                ${avatarHtml}
                <a href="/member/${encodeURIComponent(
                  account_id
                )}" class="account_id reply-account_id">${account_id}</a>
                <div class="post_id reply_id" style="display: none">${
                  reply.reply_id
                }</div>
                <div class="created_at">${formatTimeToTaipeiTime(
                  post.created_at
                )}</div>
              </div>
              <div class="menu-button">
                <i class="fa fa-ellipsis-h"></i>
                <ul class="dropdown-menu">
                  <li class="menu-item delete-post" id="delete-post">刪除</li>
                  <li class="menu-item copy-link" id="copy-link">複製連結</li>
                </ul>
              </div>
            </div>
            <div class="reply-content">
              <div class="text">${textContent}</div>
            </div>
            <div class="reply-stats">
              <div class="stat"><i class="fa fa-heart"></i> <span>${
                reply.counts.like_counts || 0
              }</span></div>
            </div>
          `;

  return replyElement;
}

export function displayMenuBtn() {
  document.body.addEventListener("click", (event) => {
    if (event.target.closest(".menu-button")) {
      event.stopPropagation(); // 阻止泡沫事件

      // 關閉菜單
      document.querySelectorAll(".dropdown-menu").forEach((menu) => {
        menu.style.display = "none";
      });

      // 切換菜單
      const dropdownMenu = event.target
        .closest(".menu-button")
        .querySelector(".dropdown-menu");
      if (dropdownMenu) {
        dropdownMenu.style.display =
          dropdownMenu.style.display === "block" ? "none" : "block";

        const postElement = event.target.closest(".post");
        const deleteButton = dropdownMenu.querySelector(".delete-post");
        const token = localStorage.getItem("userToken");
        const currentAccountId = localStorage.getItem("account_id");

        if (postElement && deleteButton) {
          const accountIdElement = postElement.querySelector(".account_id");
          if (accountIdElement) {
            const accountId = accountIdElement.textContent.trim();
            if (!token || accountId !== currentAccountId) {
              deleteButton.style.display = "none";
            } else {
              deleteButton.style.display = "block";
            }
          }
        }
      }
    }
  });
  // 點擊其他地方隱藏菜單
  document.addEventListener("click", () => {
    document.querySelectorAll(".dropdown-menu").forEach((menu) => {
      menu.style.display = "none";
    });
  });

  // 刪除
  document.body.addEventListener("click", async (event) => {
    if (event.target.classList.contains("delete-post")) {
      const postElement = event.target.closest(".post");
      const postIdElement = postElement.querySelector(".post_id");
      const token = localStorage.getItem("userToken");

      if (postElement && postIdElement) {
        const postId = postIdElement.textContent.trim();

        try {
          // fetch delete
          const response = await fetch(`/api/post/${postId}`, {
            method: "DELETE",
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });

          if (response.ok) {
            window.location.reload();
          } else {
            alert("刪除失敗，請排查問題。");
          }
        } catch (error) {
          console.error("刪除失敗:", error);
        }
      }
    }
  });

  // 複製連接
  document
    .querySelector(".postsContainer")
    .addEventListener("click", function (event) {
      const target = event.target;

      // 檢查是否點擊了複製連結按鈕
      if (target.matches(".copy-link")) {
        // 抓取 post 元素
        const postElement = target.closest(".post");

        const postIdElement = postElement.querySelector(".post_id");
        const accountIdElement = postElement.querySelector(".account_id");

        const postId = postIdElement.textContent.trim();
        const accountId = accountIdElement.textContent.trim();

        const postLink = `/member/${accountId}/post/${postId}`;
        navigator.clipboard
          .writeText(postLink)
          .then(() => {
            alert("連結已複製");
          })
          .catch((err) => {
            console.error("複製連接時出錯 ", err);
          });
      }
    });
}

function formatTimeToTaipeiTime(utcTime) {
  // 將資料庫時間（假設為 UTC-8）轉換為 UTC 時間
  const createdAtDate = new Date(utcTime);

  // 將 UTC-8 時間轉換為 UTC+8（台北時間），需加 16 小時
  const offsetHours = 8;
  const taipeiTime = new Date(
    createdAtDate.getTime() + offsetHours * 60 * 60 * 1000
  );

  // 計算當前時間與貼文時間的差異
  const now = new Date();
  const diffInMs = now - taipeiTime;
  const diffInHours = Math.floor(diffInMs / (1000 * 60 * 60));
  const diffInDays = Math.floor(diffInHours / 24);

  if (diffInHours < 24) {
    return diffInHours === 0 ? "剛剛" : `${diffInHours} 小時前`;
  } else {
    return `${diffInDays} 天前`;
  }
}

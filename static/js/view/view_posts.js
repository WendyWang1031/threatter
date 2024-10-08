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

  // 判斷 visibility 並決定圖標
  let visibilityIcon = "";
  if (post.visibility === "Public") {
    visibilityIcon = `<i class="fa-solid fa-earth-americas"></i>`;
  } else if (post.visibility === "Private") {
    visibilityIcon = `<i class="fa-solid fa-user-group"></i>`;
  }

  // 文字內容
  let userText = post.content && post.content.text ? post.content.text : "";

  userText = escapeHtml(userText);

  const textContent = convertUrlsToLinks(userText);

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
    mediaHtml += `<video controls autoplay muted loop>
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
              )}  ${visibilityIcon}</div>
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
            <div class="stat like-status">
            <i class="fa fa-heart ${post.like_state ? "liked" : ""}"></i>
            <span>${post.counts.like_counts || 0}</span></div>
            <div class="stat comment-status"><i class="fa fa-comment"></i> <span>${
              post.counts.reply_counts || 0
            }</span></div>
            
            </div>`;

  indivisial_postElement.appendChild(postElement);
  return indivisial_postElement;
}

export function displayFakeReplyContainer() {
  const section_fake_re_Element = document.createElement("div");
  section_fake_re_Element.className = "reply-title";
  section_fake_re_Element.innerHTML = `
      <div class="reply">回覆</div>      
  `;
  return section_fake_re_Element;
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

  let userText = escapeHtml(text);
  const textContent = convertUrlsToLinks(userText);

  // 媒體內容
  let mediaHtml = "";
  if (media?.images)
    mediaHtml += `<img src="${media.images}" alt="Post Image" />`;
  if (media?.videos)
    mediaHtml += `<video controls autoplay muted loop>
                    <source src="${media.videos}" type="video/mp4">
                    Your browser does not support the video tag.
                  </video>`;
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
        <div class="created_at">${formatTimeToTaipeiTime(
          comment.comment.created_at
        )}</div>
      </div>
      
      <div class="menu-button">
        <i class="fa fa-ellipsis-h"></i>
        <ul class="dropdown-menu">
          <li class="menu-item delete-post" id="delete-comment">刪除</li>
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
      <div class="stat like-status">
      <i class="fa fa-heart ${comment.comment.like_state ? "liked" : ""}"></i>
      <span>${counts.like_counts || 0}</span></div>
      <div class="stat comment-status"><i class="fa fa-comment"></i> <span>${
        counts.reply_counts || 0
      }</span></div>
      `;
  // console.log("comment.comment.:", comment.comment);
  replies.forEach((reply) => {
    const replyElement = displayReplyElement(reply);
    postElement.appendChild(replyElement);
  });

  const indivisial_postElement = document.createElement("div");
  indivisial_postElement.className = "indivisial-area Comment-Container";
  indivisial_postElement.appendChild(postElement);

  return indivisial_postElement;
}

function displayReplyElement(reply) {
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

  let userText = reply.content && reply.content.text ? reply.content.text : "";

  userText = escapeHtml(userText);

  const textContent = convertUrlsToLinks(userText);

  // 媒體內容
  let mediaHtml = "";
  if (reply.content.media?.images)
    mediaHtml += `<img src="${reply.content.media.images}" alt="Post Image" />`;
  if (reply.content.media?.videos)
    mediaHtml += `<video controls autoplay muted loop>
                    <source src="${reply.content.media.videos}" type="video/mp4">
                    Your browser does not support the video tag.
                  </video>`;
  if (reply.content.media?.audios)
    mediaHtml += `<audio controls><source src="${reply.content.media.audios}" type="audio/mpeg">Your browser does not support the audio element.</audio>`;

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
                  reply.created_at
                )}</div>
              </div>
              <div class="menu-button">
                <i class="fa fa-ellipsis-h"></i>
                <ul class="dropdown-menu">
                  <li class="menu-item delete-post" id="delete-reply">刪除</li>
                  <li class="menu-item copy-link" id="copy-link">複製連結</li>
                </ul>
              </div>
            </div>
            <div class="reply-content">
              <div class="text">${textContent}</div>
              <div class="media">${mediaHtml}</div>
              <div class="post_id reply_id" style="display: none">${
                reply.comment_id
              }</div>
            </div>
            <div class="reply-stats">
              <div class="stat like-status">
              <i class="fa fa-heart ${reply.like_state ? "liked" : ""}"></i>
              <span>${reply.counts.like_counts || 0}</span></div>
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

  // 刪除貼文
  document.body.addEventListener("click", async (event) => {
    if (event.target.id.includes("delete-post")) {
      const postElement = event.target.closest(".post");
      const postIdElement = postElement.querySelector(".post_id");
      const token = localStorage.getItem("userToken");

      if (postElement && postIdElement) {
        const postId = postIdElement.textContent.trim();
        document.getElementById("loading").classList.remove("hidden");
        try {
          // fetch delete
          const response = await fetch(`/api/post/${postId}`, {
            method: "DELETE",
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });

          if (response.ok) {
            const currentUrl = window.location.pathname;
            if (currentUrl.includes("/post/")) {
              window.location.href = "/";
            } else {
              window.location.reload();
            }
          } else {
            alert("刪除失敗，請排查問題。");
          }
        } catch (error) {
          console.error("刪除失敗:", error);
        } finally {
          document.getElementById("loading").classList.add("hidden");
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

        // 抓取當前頁面的前綴的URL並組裝
        const prefixUrl = window.location.origin;
        const postLink = `${prefixUrl}/member/${accountId}/post/${postId}`;

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

function convertUrlsToLinks(text) {
  const urlRegex = /https?:\/\/[^\s]+/g;

  return text.replace(urlRegex, function (url) {
    // 檢查是否為 YouTube 連結
    if (url.includes("youtube.com/watch?v=") || url.includes("youtu.be/")) {
      return generateYouTubeEmbed(url);
    }

    // 如果不是 YouTube 連結，直接轉換為可點擊的超連結
    return `<a href="${url}" target="_blank">${url}</a>`;
  });
}

function generateYouTubeEmbed(url) {
  let videoId = null;

  // 檢查是否為標準 YouTube 連結
  if (url.includes("youtube.com/watch?v=")) {
    const urlParams = new URLSearchParams(new URL(url).search);
    videoId = urlParams.get("v");
  }
  // 檢查是否為 YouTube 短網址
  else if (url.includes("youtu.be/")) {
    const urlObject = new URL(url);
    videoId = urlObject.pathname.split("/")[1];
  }

  if (videoId) {
    return `
      <div class="youtube-container">
        <iframe 
          width="450" 
          height="250" 
          src="https://www.youtube.com/embed/${videoId}" 
          frameborder="0" 
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
          allowfullscreen>
        </iframe>
      </div>`;
  }

  return url;
}

function escapeHtml(text) {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

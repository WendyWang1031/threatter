export function displayPostElement(post) {
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
  const textContent = post.content.text || "";

  // 媒體內容
  let mediaHtml = "";
  const media = post.content.media || {};

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
              <a href="" class="account_id">${account_id}</a>    
              </div>
              <div class="menu-button">
              <i class="fa fa-ellipsis-h"></i>
              <ul class="dropdown-menu">
                <li class="menu-item" id="delete-post">刪除</li>
                <li class="menu-item" id="copy-link">複製連結</li>
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

export function updateMessage(selector, message) {
  const element = document.getElementById(selector);
  element.textContent = message;
  element.style.display = "block";
}

export function displayPostElement(post) {
  let defaultText = "";
  const postElement = document.createElement("div");
  postElement.className = "post";
  let mediaHtml = ""; // 初始化媒體HTML

  // 根據媒體類型決定如何顯示
  if (post.image_url) {
    const url = post.image_url;
    const extension = url.split(".").pop();

    if (extension.match(/(jpg|jpeg|png|gif)$/i)) {
      mediaHtml = `<img src="${url}" alt="Post Image" />`;
    } else if (extension.match(/(mp4|webm|ogg)$/i)) {
      mediaHtml = `<video controls>
                     <source src="${url}" type="video/${extension}">
                     Your browser does not support the video tag.
                   </video>`;
    } else {
      mediaHtml = "Unsupported media type";
    }
  }
  const textContent = post.content || defaultText;
  postElement.innerHTML = `
          <div class="post-header">
            <img src="/static/images/image/user (1).png" alt="User Profile" class="profile-pic" />
            <span class="username"></span>  
          </div>
          <div class="post-content">
            <div class="text">${textContent}</div>
            <div class="media">${mediaHtml}</div>
          </div>
          <div class="post-stats">
            <div class="stat"><i class="fa fa-heart"></i> <span></span></div>
            <div class="stat"><i class="fa fa-comment"></i> <span></span></div>
            <div class="stat"><i class="fa fa-share"></i> <span></span></div>
          </div>`;
  return postElement;
}

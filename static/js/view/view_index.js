export function updateMessage(selector, message) {
  const element = document.getElementById(selector);
  element.textContent = message;
  element.style.display = "block";
}

export function displayPostElement(post) {
  let defaultText = "";
  const postElement = document.createElement("div");
  postElement.className = "post";
  let imageHtml = post.image_url
    ? `<img src="${post.image_url}" alt="Post Image" />`
    : "";
  const textContent = post.content || defaultText;
  postElement.innerHTML = `
          <div class="post-header">
            <img src="/static/images/image/user (1).png" alt="User Profile" class="profile-pic" />
            <span class="username"></span>  
          </div>
          <div class="post-content">
            <div class="text">${textContent}</div>
            <div class="media">${imageHtml}</div>
          </div>
          <div class="post-stats">
            <div class="stat"><i class="fa fa-heart"></i> <span></span></div>
            <div class="stat"><i class="fa fa-comment"></i> <span></span></div>
            <div class="stat"><i class="fa fa-share"></i> <span></span></div>
          </div>`;
  return postElement;
}

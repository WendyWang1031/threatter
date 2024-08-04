import { PermissionAllIcon } from "./view/view_icon.js";
import { displayPostElement, displayMenuBtn } from "./view/view_posts.js";

document.addEventListener("DOMContentLoaded", async function () {
  PermissionAllIcon();

  fetchGetPost();
  displayMenuBtn();
});

async function fetchGetPost() {
  const currentUrl = window.location.pathname;
  const pathSegments = currentUrl.split("/"); // 以 "/" 分割路徑成為陣列
  const accountId = pathSegments[2]; // 第三個元素為 account_id
  const postId = pathSegments[4]; // 第五個元素為 post_id

  const singlePostsUrl = `/api/member/${encodeURIComponent(
    accountId
  )}/post/${postId}`;

  try {
    const response = await fetch(singlePostsUrl);
    const result = await response.json();

    if (result) {
      const postsContainer = document.querySelector(".postsContainer");

      const postElement = displayPostElement(result);
      postsContainer.appendChild(postElement);
    }
  } catch (error) {
    console.error("Error fetching post data:", error);
  }
}

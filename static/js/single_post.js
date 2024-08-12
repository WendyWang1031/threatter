import { PermissionAllIcon } from "./view/view_icon.js";
import {
  displayContentElement,
  displayCommentElement,
  displayMenuBtn,
} from "./view/view_posts.js";

document.addEventListener("DOMContentLoaded", async function () {
  PermissionAllIcon();

  fetchGetPost();
  fetchGetCommentAndReply();
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

      const postElement = displayContentElement(result);
      postsContainer.appendChild(postElement);
    }
  } catch (error) {
    console.error("Error fetching post data:", error);
  }
}

async function fetchGetCommentAndReply() {
  const currentUrl = window.location.pathname;
  const pathSegments = currentUrl.split("/"); // 以 "/" 分割路徑成為陣列
  const accountId = pathSegments[2]; // 第三個元素為 account_id
  const postId = pathSegments[4]; // 第五個元素為 post_id

  const commentAndReplyUrl = `/api/member/${encodeURIComponent(
    accountId
  )}/post/${postId}/detail`;

  try {
    const response = await fetch(commentAndReplyUrl);
    const result = await response.json();

    if (result) {
      const commentContainer = document.querySelector(
        ".single-CommentContainer"
      );
      // console.log("result:", result);
      result.data.forEach((comment) => {
        const commentElement = displayCommentElement(comment);
        commentContainer.appendChild(commentElement);
      });
    }
  } catch (error) {
    console.error("Error fetching comment data:", error);
  }
}

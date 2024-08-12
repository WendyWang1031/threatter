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

let currentPage = 0;
let hasNextPage = true;
let isWaitingForData = false;

const observer = new IntersectionObserver(
  (entries) => {
    const firstEntry = entries[0];

    if (firstEntry.isIntersecting && hasNextPage && !isWaitingForData) {
      //調用fetch函式的時候使用非同步加載
      fetchGetCommentAndReply();
    }
  },
  { threshold: 0.5 }
);

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
    console.error("Error fetching single post data:", error);
  }
}

async function fetchGetCommentAndReply() {
  document.getElementById("loading").classList.remove("hidden");

  const currentUrl = window.location.pathname;
  const pathSegments = currentUrl.split("/"); // 以 "/" 分割路徑成為陣列
  const accountId = pathSegments[2]; // 第三個元素為 account_id
  const postId = pathSegments[4]; // 第五個元素為 post_id

  const commentAndReplyUrl = `/api/member/${encodeURIComponent(
    accountId
  )}/post/${postId}/detail?page=${currentPage}`;

  try {
    isWaitingForData = true;
    const response = await fetch(commentAndReplyUrl);
    const result = await response.json();

    let lastItem = document.querySelector(".Comment-Container:last-child");
    if (result && result.data.length > 0) {
      console.log("result next_page:", result.next_page);
      currentPage++;
      hasNextPage = result.next_page != null;

      const commentContainer = document.querySelector(
        ".single-CommentContainer"
      );
      // console.log("result:", result);
      result.data.forEach((comment) => {
        const commentElement = displayCommentElement(comment);
        commentContainer.appendChild(commentElement);
      });

      let newItem = document.querySelector(".Comment-Container:last-child");
      if (lastItem) observer.unobserve(lastItem);
      if (hasNextPage) {
        if (newItem) observer.observe(newItem);
      }
    } else {
      hasNextPage = false;
    }
    isWaitingForData = false;
  } catch (error) {
    console.error("Error fetching comment data:", error);
    isWaitingForData = false;
  } finally {
    document.getElementById("loading").classList.add("hidden");
  }
}

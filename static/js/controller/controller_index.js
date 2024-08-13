import { displayMemberDetail } from "../view/view_index.js";
import { PermissionAllIcon } from "../view/view_icon.js";
import { likePost } from "./controller_like.js";
import { validateForm } from "./controller_submit_item.js";

import { displayContentElement, displayMenuBtn } from "../view/view_posts.js";

import {
  closeCreatePost,
  previewCreatePost,
  displayCreatePost,
} from "../view/view_post_detail.js";

const postHomeURL = "/api/post/home";

let currentPage = 0;
let hasNextPage = true;
let isWaitingForData = false;

document.addEventListener("DOMContentLoaded", async function () {
  PermissionAllIcon();

  await fetchGetMemberDetail();
  // 更新貼文內容
  fetchGetPost();
  likePost();

  closeCreatePost();
  displayCreatePost();
  previewCreatePost();

  displayMenuBtn();
  selectSinglePost(event);

  // 首頁：提交貼文按鈕
  const submitPostButton = document.querySelector(".submit-post-btn");
  submitPostButton.addEventListener("click", function (event) {
    event.preventDefault();
    validateForm("post", null, null, null);
  });
});

async function fetchGetPost() {
  try {
    //開始新的資料加載前設定
    isWaitingForData = true;

    const token = localStorage.getItem("userToken");
    const headers = token ? { Authorization: `Bearer ${token}` } : {};

    const response = await fetch(`${postHomeURL}?page=${currentPage}`, {
      headers: headers,
    });
    const result = await response.json();

    let lastItem = document.querySelector(".indivisial-area:last-child");
    if (result && result.data.length > 0) {
      currentPage++;
      hasNextPage = result.next_page != null;

      const postsContainer = document.querySelector(".postsContainer");
      result.data.forEach((post) => {
        const postElement = displayContentElement(post);
        postsContainer.appendChild(postElement);
      });

      let newItem = document.querySelector(".indivisial-area:last-child");
      if (lastItem) observer.unobserve(lastItem);
      if (hasNextPage) {
        if (newItem) observer.observe(newItem);
      }
    } else {
      hasNextPage = false;
    }
    isWaitingForData = false;
  } catch (error) {
    console.error("Error fetching post data:", error);
    isWaitingForData = false;
  }
}

async function fetchGetMemberDetail() {
  const account_id = localStorage.getItem("account_id");
  const memberUrl = `/api/member/${encodeURIComponent(account_id)}`;
  if (!account_id) {
    console.log("User not logged in, using default avatar.");
    return;
  }
  try {
    const response = await fetch(memberUrl);
    const result = await response.json();

    if (result) {
      displayMemberDetail(result);
    } else {
      console.error("Failed to retrieve post data.");
    }
  } catch (error) {
    console.error("Error fetching post data:", error);
  }
}

const observer = new IntersectionObserver(
  (entries) => {
    const firstEntry = entries[0];

    if (firstEntry.isIntersecting && hasNextPage && !isWaitingForData) {
      //調用fetch函式的時候使用非同步加載
      fetchGetPost();
    }
  },
  { threshold: 0.5 }
);

function selectSinglePost() {
  document
    .querySelector(".postsContainer")
    .addEventListener("click", (event) => {
      // 確認點擊的元素或其父元素是否是 .post

      const post_header = event.target.closest(".post-header");
      const post_content = event.target.closest(".post-content");

      // 檢查是否點擊了 menu-button 或其子元素
      const menuButton = event.target.closest(".menu-button");
      if (menuButton) {
        return; // 直接返回，不進行後續處理
      }

      if (post_header || post_content) {
        console.log("Post clicked via delegation:", post_header, post_content);
        event.preventDefault(); // 阻止默認行為

        // 獲取 account_id 和 post_id
        const postElement = event.target.closest(".post");
        const accountIdElement = postElement.querySelector(".account_id");
        const postIdElement = postElement.querySelector(".post_id");

        if (accountIdElement && postIdElement) {
          const accountId = accountIdElement.textContent.trim();
          const postId = postIdElement.textContent.trim();
          const targetUrl = `/member/${encodeURIComponent(
            accountId
          )}/post/${encodeURIComponent(postId)}`;
          console.log("Navigating to:", targetUrl);
          window.location.href = targetUrl;
        } else {
          console.error("accountId or postId is missing");
        }
      }
    });
}

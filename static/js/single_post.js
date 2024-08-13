import { PermissionAllIcon } from "./view/view_icon.js";
import { displayMemberDetail } from "./view/view_index.js";
import {
  displayContentElement,
  displayCommentElement,
  displayFakeReplyContainer,
  displayMenuBtn,
} from "./view/view_posts.js";

import {
  closeCreatePost,
  previewCreatePost,
  displayCreateComment,
} from "./view/view_post_detail.js";

import { validateForm } from "./controller/controller_submit_item.js";

import { likePost, likeCommentAndReply } from "./controller/controller_like.js";

document.addEventListener("DOMContentLoaded", async function () {
  PermissionAllIcon();
  fetchGetMemberDetail();

  fetchGetPost();
  likePost();
  fetchGetCommentAndReply();

  likeCommentAndReply();

  submitComment();

  closeCreatePost();
  previewCreatePost();
  displayCreateComment();

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

  const token = localStorage.getItem("userToken");
  const headers = token ? { Authorization: `Bearer ${token}` } : {};

  const singlePostsUrl = `/api/member/${encodeURIComponent(
    accountId
  )}/post/${postId}`;

  try {
    const response = await fetch(singlePostsUrl, {
      headers: headers,
    });
    const result = await response.json();

    if (result) {
      // console.log("result:", result);
      const postsContainer = document.querySelector(".postsContainer");

      const postElement = displayContentElement(result);
      postsContainer.appendChild(postElement);

      const fake_reply_container = document.querySelector(".reply-header");
      const fakeElement = displayFakeReplyContainer();
      fake_reply_container.appendChild(fakeElement);
    }
  } catch (error) {
    console.error("Error fetching single post data:", error);
  }
}

async function fetchGetCommentAndReply() {
  document.getElementById("loading").classList.remove("hidden");

  const token = localStorage.getItem("userToken");
  const headers = token ? { Authorization: `Bearer ${token}` } : {};

  const currentUrl = window.location.pathname;
  const pathSegments = currentUrl.split("/"); // 以 "/" 分割路徑成為陣列
  const accountId = pathSegments[2]; // 第三個元素為 account_id
  const postId = pathSegments[4]; // 第五個元素為 post_id

  const commentAndReplyUrl = `/api/member/${encodeURIComponent(
    accountId
  )}/post/${postId}/detail?page=${currentPage}`;

  try {
    isWaitingForData = true;

    const response = await fetch(commentAndReplyUrl, {
      headers: headers,
    });
    const result = await response.json();

    let lastItem = document.querySelector(".Comment-Container:last-child");
    if (result && result.data.length > 0) {
      // console.log("result next_page:", result.next_page);
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

function submitComment() {
  const submitCommentButton = document.querySelector(".submit-post-btn");
  submitCommentButton.addEventListener("click", function (event) {
    event.preventDefault();
    const currentUrl = window.location.pathname;
    const pathSegments = currentUrl.split("/"); // 以 "/" 分割路徑成為陣列
    const accountId = pathSegments[2]; // 第三個元素為 account_id
    const postId = pathSegments[4]; // 第五個元素為 post_id
    validateForm("comment", accountId, postId, null);
  });
}

import { PermissionAllIcon } from "./view/view_icon.js";
import { displayMemberDetail } from "./view/view_index.js";
import {
  displayContentElement,
  displayCommentElement,
  displayFakeReplyContainer,
  displayMenuBtn,
} from "./view/view_posts.js";

import { closeCreatePost, previewCreatePost } from "./view/view_post_detail.js";

import { validateForm } from "./controller/controller_submit_item.js";
import {
  deleteComment,
  deleteReply,
} from "./controller/controller_delete_comment_reply.js";

import { likePost, likeCommentAndReply } from "./controller/controller_like.js";

document.addEventListener("DOMContentLoaded", async function () {
  PermissionAllIcon();
  fetchGetMemberDetail();

  fetchGetPost();
  likePost();
  fetchGetCommentAndReply();

  likeCommentAndReply();
  deleteComment();
  deleteReply();

  submitForm();

  closeCreatePost();
  previewCreatePost();
  displayCreateCommentAndReply();

  displayMenuBtn();
});

let currentPage = 0;
let hasNextPage = true;
let isWaitingForData = false;

let currentAction = "comment";
let currentReplyID = null;

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

    if (result.message === "沒有留言資料") {
      const replyContainer = document.querySelector(".reply-title");
      const noData = document.createElement("div");
      noData.className = "no-data";
      const noDataMessage = document.createElement("div");
      noDataMessage.className = "no-data-message";
      noDataMessage.textContent = "尚無任何留言。";

      noData.appendChild(noDataMessage);
      replyContainer.appendChild(noData);
    }

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

function submitForm() {
  const submitButton = document.querySelector(".submit-post-btn");
  submitButton.addEventListener("click", function (event) {
    event.preventDefault();

    const currentUrl = window.location.pathname;
    const pathSegments = currentUrl.split("/"); // 以 "/" 分割路徑成為陣列
    const accountId = pathSegments[2]; // 第三個元素為 account_id
    const postId = pathSegments[4]; // 第五個元素為 post_id

    if (currentAction === "comment") {
      validateForm("comment", accountId, postId, null);
    } else if (currentAction === "reply" && currentReplyID) {
      validateForm("reply", accountId, postId, currentReplyID);
    } else {
      console.error("Reply ID is missing");
    }
  });
}

function displayCreateCommentAndReply() {
  const token = localStorage.getItem("userToken");
  const createPosterCard = document.querySelector(".create-poster-card");
  const signin_mask = document.querySelector(".signin-mask");

  document
    .querySelector(".postsContainer")
    .addEventListener("click", (event) => {
      console.log("click comment");
      const commentBtn = event.target.closest(".fa-comment");

      if (commentBtn) {
        currentAction = "comment";
        if (!token) {
          signin_mask.style.display = "flex";
        } else {
          createPosterCard.style.display = "flex";
        }
      }
    });

  document
    .querySelector(".single-CommentContainer")
    .addEventListener("click", (event) => {
      const replyBtn = event.target.closest(".fa-comment");
      if (!replyBtn) {
        return;
      }

      currentAction = "reply";

      const commentElement = replyBtn.closest(".indivisial-area");
      const replyElement = commentElement.querySelector(".message_id");

      // console.log("commentElement:", commentElement);
      // console.log("replyElement:", replyElement);

      if (replyElement) {
        currentReplyID = replyElement.textContent.trim();
      } else {
        console.error("Reply ID element not found");
      }

      if (!token) {
        signin_mask.style.display = "flex";
      } else {
        createPosterCard.style.display = "flex";
      }
    });
}

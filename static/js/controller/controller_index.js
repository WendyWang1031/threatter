import { displayMemberDetail } from "../view/view_index.js";
import { PermissionAllIcon } from "../view/view_icon.js";
import { likePost } from "./controller_like.js";
import { validateForm } from "./controller_submit_item.js";

import { displayContentElement, displayMenuBtn } from "../view/view_posts.js";
import { checkUserState } from "./controller_auth.js";
import { selectSinglePost } from "./controller_select_single_post.js";

import {
  closeCreatePost,
  previewCreatePost,
  displayCreatePost,
} from "../view/view_post_detail.js";

const postHomeURL = "/api/post/home";
const postHomeRecommendationURL = "/api/post/home/recommendation";

let currentPage = 0;
let hasNextPage = true;
let isWaitingForData = false;

document.addEventListener("DOMContentLoaded", async function () {
  PermissionAllIcon();
  await checkUserState();

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

    //關係推薦貼文
    let recommendationResponse, recommendationResult;
    if (token) {
      recommendationResponse = await fetch(
        `${postHomeRecommendationURL}?page=${currentPage}`,
        {
          headers: headers,
        }
      );
      recommendationResult = await recommendationResponse.json();
    }

    const postResponse = await fetch(`${postHomeURL}?page=${currentPage}`, {
      headers: headers,
    });
    const postResult = await postResponse.json();

    const result = {
      data: [],
      next_page: postResult.next_page,
    };

    if (recommendationResult && recommendationResult.data.length > 0) {
      result.data = [...recommendationResult.data, ...postResult.data];
    } else {
      result.data = postResult.data;
    }

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
  console.log("fetchGetMemberDetail called");
  const account_id = localStorage.getItem("account_id");
  console.log("account_id:", account_id);
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
      console.error("Failed to retrieve member data.");
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

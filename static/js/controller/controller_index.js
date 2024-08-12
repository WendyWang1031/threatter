import {
  displayCreatePostAccount,
  previewCreatePost,
  displayCreatePost,
  displayMemberDetail,
} from "../view/view_index.js";
import { PermissionAllIcon } from "../view/view_icon.js";
import { uploadMediaFile } from "./controller_upload.js";

import { displayContentElement, displayMenuBtn } from "../view/view_posts.js";

import { closeCreatePost } from "../view/view_closePost.js";

const postURL = "/api/post";
const postHomeURL = "/api/post/home";

let currentPage = 0;
let hasNextPage = true;
let isWaitingForData = false;

document.addEventListener("DOMContentLoaded", async function () {
  displayCreatePost();
  PermissionAllIcon();
  closeCreatePost();
  await fetchGetMemberDetail();
  // 更新貼文內容
  fetchGetPost();
  previewCreatePost();
  displayMenuBtn();
  selectSinglePost(event);

  // 提交貼文按鈕
  const submitPostButton = document.querySelector(".submit-post-btn");
  submitPostButton.addEventListener("click", function (event) {
    event.preventDefault();
    validateForm();
  });
});

function validateForm() {
  const content = document.querySelector(".post-input").value;

  // 初始媒體類型的值
  let imageFile = null;
  let videoFile = null;
  let audioFile = null;

  // 抓取所有媒體類型
  const imageUploadInput = document.getElementById("image-upload");
  const videoUploadInput = document.getElementById("video-upload");
  const audioUploadInput = document.getElementById("audio-upload");

  if (imageUploadInput.files.length > 0) {
    imageFile = imageUploadInput.files[0];
  }
  if (videoUploadInput.files.length > 0) {
    videoFile = videoUploadInput.files[0];
  }
  if (audioUploadInput.files.length > 0) {
    audioFile = audioUploadInput.files[0];
  }
  console.log("videoUploadInput:", videoUploadInput);

  if (content === "" && !imageFile && !videoFile && !audioFile) {
    alert("請填寫文字欄位或上傳圖片、影片或音源");
    return false;
  }
  submitPost(content, imageFile, videoFile, audioFile);
  return true;
}

async function submitPost(content, imageFile, videoFile, audioFile) {
  document.getElementById("loading").classList.remove("hidden");
  let postData = {
    post_parent_id: null,
    content: {
      text: content,
      media: {
        images: null,
        videos: null,
        audios: null,
      },
    },
    visibility: "public",
  };

  // 圖片
  if (imageFile) {
    const imageUrl = await uploadMediaFile(imageFile);
    if (imageUrl) {
      postData.content.media.images = imageUrl;
    }
  }

  // 影片
  if (videoFile) {
    const videoUrl = await uploadMediaFile(videoFile);
    if (videoUrl) {
      postData.content.media.videos = videoUrl;
    }
  }

  // 音檔
  if (audioFile) {
    const audioUrl = await uploadMediaFile(audioFile);
    if (audioUrl) {
      postData.content.media.audios = audioUrl;
    }
  }

  try {
    await fetchUpdatePost(postData);
  } catch (error) {
    console.error("Error submitting post:", error);
    alert("Failed to submit post: " + error.message);
  } finally {
    document.getElementById("loading").classList.add("hidden");
  }
}

async function fetchUpdatePost(postData) {
  document.getElementById("loading").classList.remove("hidden");
  const token = localStorage.getItem("userToken");

  try {
    const response = await fetch(postURL, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(postData),
    });

    console.log("body:", JSON.stringify(postData));

    if (!response.ok) {
      console.log("Failed to post details:", response.status);

      throw new Error(`HTTP status ${response.status}`);
    } else {
      window.location = "/";
    }
  } catch (error) {
    console.error("Error updating post data", error);
  } finally {
    document.getElementById("loading").classList.add("hidden");
  }
}

async function fetchGetPost() {
  try {
    //開始新的資料加載前設定
    isWaitingForData = true;

    const response = await fetch(`${postHomeURL}?page=${currentPage}`);
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

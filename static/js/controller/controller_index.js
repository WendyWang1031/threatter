import {
  displayPostElement,
  previewCreatePost,
  displayCreatePostAccount,
  displayCreatePost,
} from "../view/view_index.js";
import {
  getPresignedUrl,
  uploadFileToS3,
  uploadMediaFile,
} from "./controller_upload.js";

import { closeCreatePost } from "./controller_createPost.js";

const postURL = "/api/post";
const postHomeURL = "/api/post/home";

document.addEventListener("DOMContentLoaded", async function () {
  displayCreatePost();
  closeCreatePost();
  await displaymemberDetail();
  // 更新貼文內容
  fetchGetPost();

  // 提交貼文按鈕
  const submitPostButton = document.querySelector(".submit-post-btn");
  submitPostButton.addEventListener("click", function (event) {
    event.preventDefault();
    validateForm();
  });
});

function validateForm() {
  const form = document.querySelector(".post-form");
  const content = form.querySelector("textarea").value;

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
  console.log("postData:", postData);

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
  }
}

async function fetchUpdatePost(postData) {
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

    if (!response.ok) {
      console.log("Failed to post details:", response.status);

      throw new Error(`HTTP status ${response.status}`);
    } else {
      window.location = "/";
    }
  } catch (error) {
    console.error("Error updating post data", error);
  } finally {
  }
}

async function fetchGetPost() {
  try {
    const response = await fetch(postHomeURL);

    const result = await response.json();

    if (result) {
      const postsContainer = document.querySelector(".postsContainer");
      result.data.forEach((post) => {
        const postElement = displayPostElement(post);
        postsContainer.appendChild(postElement);
      });
    } else {
      console.error("Failed to retrieve post data.");
    }
  } catch (error) {
    console.error("Error fetching post data:", error);
  }
}

async function displaymemberDetail() {
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
      const accountIdSpan = document.querySelector(".account_id");
      accountIdSpan.textContent = result.account_id;

      const avatar = document.querySelector(".profile-pic");
      const img = document.createElement("img");
      img.src = result.avatar;
      img.classList.add("profile-pic");
      avatar.replaceWith(img);
    } else {
      console.error("Failed to retrieve post data.");
    }
  } catch (error) {
    console.error("Error fetching post data:", error);
  }
}

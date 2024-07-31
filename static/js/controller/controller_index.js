import { displayPostElement, previewCreatePost } from "../view/view_index.js";
import { getPresignedUrl, uploadFileToS3 } from "./controller_upload.js";

const postURL = "/api/post";
const postHomeURL = "/api/post/home";

document.addEventListener("DOMContentLoaded", function () {
  // 更新貼文內容
  fetchGetPost();
  // document
  //   .getElementById("file-input")
  //   .addEventListener("change", previewCreatePost);

  // 提交貼文按鈕
  const submitPostButton = document.querySelector(".submit-post-btn");
  submitPostButton.addEventListener("click", function (event) {
    event.preventDefault();
    validateForm();
  });
});

async function submitPost(content, file) {
  console.log("file:", file);
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

  if (file) {
    try {
      const urls = await getPresignedUrl(file.name, file.type);
      await uploadFileToS3(urls.presigned_url, file);

      // 根據類型設定對應的 media 字段
      if (file.type.startsWith("image/")) {
        postData.content.media.images = urls.cdn_url;
      } else if (file.type.startsWith("video/")) {
        postData.content.media.videos = urls.cdn_url;
      } else if (file.type.startsWith("audio/")) {
        postData.content.media.audios = urls.cdn_url;
      }
    } catch (error) {
      console.log("Error uploading file: " + error.message);
      return;
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
    console.log("GET response:", response);
    const result = await response.json();
    console.log("GET result:", result);

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

  if (
    content === "" &&
    imageUploadInput === 0 &&
    videoUploadInput === 0 &&
    audioUploadInput === 0
  ) {
    alert("請填寫文字欄位或上傳圖片、影片或音源");
    return false;
  }
  submitPost(content, imageFile, videoFile, audioFile);
}

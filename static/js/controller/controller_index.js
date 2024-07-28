import { displayPostElement, previewCreatePost } from "../view/view_index.js";
import { getPresignedUrl, uploadFileToS3 } from "./controller_upload.js";
document.addEventListener("DOMContentLoaded", function () {
  // 更新貼文內容
  fetchGetPost();

  document
    .getElementById("file-input")
    .addEventListener("change", previewCreatePost);

  // 提交貼文按鈕
  const submitButton = document.querySelector(".send-button");
  submitButton.addEventListener("click", function (event) {
    event.preventDefault();
    const form = document.querySelector(".post-form");
    const content = form.querySelector("[name='text']").value;
    const file = form.querySelector("[name='img']").files[0];
    submitPost(content, file);
  });
});

const postURL = "/api/post_test";

async function submitPost(content, file) {
  let postData = { content };
  console.log("file:", file);

  if (file) {
    try {
      const urls = await getPresignedUrl(file.name, file.type);

      await uploadFileToS3(urls.presigned_url, file);

      postData.image_url = urls.cdn_url;
    } catch (error) {
      console.log("Error uploading file 1: " + error.message);
      return;
    }
  } else {
    postData.image_url = null;
  }
  try {
    await fetchUpdatePost(postData);
  } catch (error) {
    console.error("Error submitting post:", error);
    alert("Failed to submit post: " + error.message);
  }
}

async function fetchUpdatePost(postData) {
  console.log("postData2:", postData);
  if (!validateForm()) {
    return;
  }

  try {
    const response = await fetch(postURL, {
      method: "POST",
      headers: {
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
    const response = await fetch(postURL);
    const result = await response.json();

    if (result.ok && result.data) {
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
  const textInput = document.getElementById("text").value.trim();
  const fileInput = document.getElementById("img").files.length;

  if (textInput === "" && fileInput === 0) {
    alert("請填寫文字欄位或上傳圖片");
    return false;
  }
  return true;
}

import { displayPostElement } from "../view/view_index.js";
document.addEventListener("DOMContentLoaded", function () {
  fetchGetPost();

  const submitButton = document.querySelector(".send-button");
  submitButton.addEventListener("click", fetchUpdatePost);
});

const postURL = "/api/post";

async function fetchUpdatePost() {
  const form = document.querySelector(".post-form");

  const formData = new FormData(form);

  if (!validateForm()) {
    return;
  }

  try {
    const response = await fetch(postURL, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      console.log("Failed to post details:", response.status);

      throw new Error(`HTTP status ${response.status}`);
    } else {
      // window.location.reload();
    }
  } catch (error) {
    console.error("Error updating profile", error);
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

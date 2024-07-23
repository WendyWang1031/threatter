document.addEventListener("DOMContentLoaded", function () {
  fetchGetPost();

  const submitButton = document.querySelector('button[type="button"]');
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
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      console.log("Failed to post details:", response.status);

      throw new Error(`HTTP status ${response.status}`);
    } else {
      window.location.reload();
    }
  } catch (error) {
    console.error("Error updating profile");
  } finally {
  }
}

async function fetchGetPost() {
  try {
    const response = await fetch(postURL);
    const result = await response.json();
    console.log(result);

    if (result.ok && result.data) {
      const postsContainer = document.querySelector(".postsContainer");
      const postElement = document.createElement("div");
      postElement.className = "post";

      result.data.forEach((post) => {
        const postElement = document.createElement("div");
        postElement.className = "post";

        postElement.innerHTML = `
          <div class="post-header">
            <img src="/static/images/image/user (1).png" alt="User Profile" class="profile-pic" />
            <span class="username"></span>  
          </div>
          <div class="post-content">
            <div class="text">${post.content}</div>
            <div class="media">
              <img src="${post.image_url}" alt="Post Image" />
            </div>
          </div>
          <div class="post-stats">
            <div class="stat"><i class="fa fa-heart"></i> <span></span></div>
            <div class="stat"><i class="fa fa-comment"></i> <span></span></div>
            <div class="stat"><i class="fa fa-share"></i> <span></span></div>
          </div>`;

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

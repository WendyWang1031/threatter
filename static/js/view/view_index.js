export function updateMessage(selector, message) {
  const element = document.getElementById(selector);
  element.textContent = message;
  element.style.display = "block";
}

export function displayCreatePostAccount() {
  const account_id_value = localStorage.getItem("account_id");
  const account_id = document.querySelector(".account_id");
  account_id.textContent = account_id_value;
}

export function previewCreatePost(event) {
  const file = event.target.files[0];
  const preview = document.getElementById("preview");
  if (file) {
    const reader = new FileReader();

    reader.onload = function (e) {
      const url = e.target.result;
      if (file.type.startsWith("image/")) {
        preview.innerHTML = `<img src="${url}" alt="Image preview">`;
      } else if (file.type.startsWith("video/")) {
        preview.innerHTML = `<video src="${url}" controls></video>`;
      } else if (file.type.startsWith("audio/")) {
        preview.innerHTML = `<audio src="${url}" controls></audio>`;
      }
    };

    reader.readAsDataURL(file);
  }
}

export function displayCreatePost() {
  const token = localStorage.getItem("userToken");

  const userPostContainer = document.querySelector(".user-post-container");
  const createPosterCard = document.querySelector(".create-poster-card");
  const plusBtn = document.querySelector(".create-post-btn");
  const notify = document.querySelector(".heart");
  const memeber = document.querySelector(".profile");
  const profileIcon = document.querySelector(".icon.profile");

  const signin_mask = document.querySelector(".signin-mask");

  if (!token) {
    userPostContainer.addEventListener("click", function () {
      signin_mask.style.display = "flex";
    });
    plusBtn.addEventListener("click", function () {
      signin_mask.style.display = "flex";
    });
    notify.addEventListener("click", function () {
      signin_mask.style.display = "flex";
    });
    memeber.addEventListener("click", function () {
      signin_mask.style.display = "flex";
    });
  } else {
    const account_id = localStorage.getItem("account_id");
    userPostContainer.addEventListener("click", function () {
      createPosterCard.style.display = "flex";
    });
    plusBtn.addEventListener("click", function () {
      createPosterCard.style.display = "flex";
    });
    profileIcon.addEventListener("click", function () {
      const memberUrl = `/member/${encodeURIComponent(account_id)}`;
      window.location.href = memberUrl;
    });
  }
}

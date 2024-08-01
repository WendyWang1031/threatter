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

  if (!token) {
    userPostContainer.addEventListener("click", function () {
      signin_mask.style.display = "flex";
    });
    plusBtn.addEventListener("click", function () {
      signin_mask.style.display = "flex";
    });
  } else {
    userPostContainer.addEventListener("click", function () {
      createPosterCard.style.display = "flex";
    });
    plusBtn.addEventListener("click", function () {
      createPosterCard.style.display = "flex";
    });
  }
}

export function displayMemberDetail(data) {
  const accountIdSpan = document.querySelector(".account_id");
  accountIdSpan.textContent = data.account_id;
  if (data.avatar) {
    const avatar = document.querySelector(".profile-pic");
    const img = document.createElement("img");
    img.src = data.avatar;
    img.classList.add("profile-pic");
    avatar.replaceWith(img);
  } else {
    const icon = document.createElement("i");
    icon.classList.add("fa-regular", "fa-circle-user", "profile-pic");
  }
}

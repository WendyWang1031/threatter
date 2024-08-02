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
  const imageUploadInput = document.getElementById("image-upload");
  const videoUploadInput = document.getElementById("video-upload");
  const audioUploadInput = document.getElementById("audio-upload");

  const mediaPreviewContainer = document.getElementById("media-preview");

  // 文件選擇處理
  function handleFileSelect(event) {
    const file = event.target.files[0];
    if (!file) return;

    mediaPreviewContainer.innerHTML = "";

    const fileType = file.type.split("/")[0];
    const reader = new FileReader();

    reader.onload = function (e) {
      let mediaElement;

      // 不同媒體類型
      switch (fileType) {
        case "image":
          mediaElement = document.createElement("img");
          mediaElement.src = e.target.result;
          break;
        case "video":
          mediaElement = document.createElement("video");
          mediaElement.src = e.target.result;
          mediaElement.controls = true;
          break;
        case "audio":
          mediaElement = document.createElement("audio");
          mediaElement.src = e.target.result;
          mediaElement.controls = true;
          break;
        default:
          mediaElement = document.createTextNode("Unsupported media type.");
      }

      // 樣式
      if (mediaElement) {
        mediaElement.style.maxWidth = "100%";
        mediaElement.style.maxHeight = "200px";
        mediaElement.style.borderRadius = "10px";
        mediaElement.style.marginTop = "10px";
      }

      mediaPreviewContainer.appendChild(mediaElement);
    };

    if (fileType === "image" || fileType === "video" || fileType === "audio") {
      reader.readAsDataURL(file);
    }
  }

  imageUploadInput.addEventListener("change", handleFileSelect);
  videoUploadInput.addEventListener("change", handleFileSelect);
  audioUploadInput.addEventListener("change", handleFileSelect);
}

export function displayCreatePost() {
  const token = localStorage.getItem("userToken");

  const userPostContainer = document.querySelector(".user-post-container");
  const createPosterCard = document.querySelector(".create-poster-card");
  const plusBtn = document.querySelector(".create-post-btn");
  const signin_mask = document.querySelector(".signin-mask");

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
    const avatarCreatePost = document.querySelector(".profile-pic-create-post");
    if (avatarCreatePost) {
      const imgCreatePost = document.createElement("img");
      imgCreatePost.src = data.avatar;
      imgCreatePost.classList.add("profile-pic");
      avatarCreatePost.replaceWith(imgCreatePost);
    }

    const avatarUserInfoPost = document.querySelector(".user-info-profile-pic");
    if (avatarUserInfoPost) {
      const imgUserInfoPost = document.createElement("img");
      imgUserInfoPost.src = data.avatar;
      imgUserInfoPost.classList.add("profile-pic");
      avatarUserInfoPost.replaceWith(imgUserInfoPost);
    }
  } else {
    const icon = document.createElement("i");
    icon.classList.add("fa-regular", "fa-circle-user", "profile-pic");
  }
}

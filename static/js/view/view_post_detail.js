export function closeCreatePost() {
  const createPosterCard = document.querySelector(".create-poster-card");
  const postForm = document.querySelector(".post-form");
  const mediaPreviewContainer = document.getElementById("media-preview");
  // console.log("postForm:", postForm);

  // 點擊遮罩地方可以關閉
  createPosterCard.addEventListener("click", function (event) {
    if (event.target === createPosterCard) {
      createPosterCard.style.display = "none";

      postForm.reset();

      const errorMessage = document.querySelector(".error-message");
      errorMessage.style.display = "none";

      // 清空所有值
      const fileInputs = postForm.querySelectorAll('input[type="file"]');
      fileInputs.forEach((input) => {
        input.value = "";
      });

      const textarea = postForm.querySelector(".post-input");
      if (textarea) {
        textarea.value = "";
      }

      // 清空Media
      if (mediaPreviewContainer) {
        mediaPreviewContainer.innerHTML = "";
      }
    }
  });
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

  const userPostContainer = document.querySelector(".user-post-container-fake");
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
      const account_id = localStorage.getItem("account_id");
      console.log("account_id:", account_id);
      const userName = localStorage.getItem("userName");
      console.log("userName:", userName);
      createPosterCard.style.display = "flex";
    });
    plusBtn.addEventListener("click", function () {
      const account_id = localStorage.getItem("account_id");
      const userName = localStorage.getItem("userName");
      createPosterCard.style.display = "flex";
    });
  }
}

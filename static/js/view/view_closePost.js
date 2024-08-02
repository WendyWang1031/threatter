export function closeCreatePost() {
  const createPosterCard = document.querySelector(".create-poster-card");
  const postForm = document.querySelector(".post-form");
  const mediaPreviewContainer = document.getElementById("media-preview");
  console.log("postForm:", postForm);

  // 點擊遮罩地方可以關閉
  createPosterCard.addEventListener("click", function (event) {
    if (event.target === createPosterCard) {
      createPosterCard.style.display = "none";

      postForm.reset();

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

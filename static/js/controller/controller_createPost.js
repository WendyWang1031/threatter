export function closeCreatePost() {
  const createPosterCard = document.querySelector(".create-poster-card");
  const postForm = document.querySelector(".post-form");

  // 點擊遮罩地方可以關閉
  createPosterCard.addEventListener("click", function (event) {
    if (event.target === createPosterCard) {
      closeModal();
    }
  });

  // 關閉
  function closeModal() {
    createPosterCard.style.display = "none";
    postForm.reset();
  }
}

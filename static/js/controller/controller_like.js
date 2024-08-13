export function likePost() {
  document
    .querySelector(".postsContainer")
    .addEventListener("click", (event) => {
      const likeIcon = event.target.closest(".fa-heart");

      if (likeIcon) {
        // console.log("Post clicked via delegation:", like_post);
        event.preventDefault(); // 阻止默認行為

        // 獲取 account_id 和 post_id
        const postElement = event.target.closest(".post");
        const accountIdElement = postElement.querySelector(".account_id");
        const postIdElement = postElement.querySelector(".post_id");

        if (accountIdElement && postIdElement) {
          const accountId = accountIdElement.textContent.trim();
          const postId = postIdElement.textContent.trim();

          // 檢查當前是否已經點讚（通過檢查圖標顏色或狀態）
          const isLiked = likeIcon.classList.contains("liked");

          // 立即更新圖標狀態
          likeIcon.classList.toggle("liked", !isLiked);

          // 抓取當前的讚數並更新
          const likeCountElement = likeIcon.nextElementSibling; // 抓取 <span> 元素
          let likeCount = parseInt(likeCountElement.textContent, 10); // 將文字轉換為十進制數字
          if (!isLiked) {
            likeCount += 1;
          } else {
            likeCount -= 1;
          }
          likeCountElement.textContent = likeCount; // 更新數字顯示

          // 構建請求數據
          const likePostData = { like: !isLiked };

          // 更新點讚狀態
          fetchUpdateLike(accountId, postId, likePostData).catch((error) => {
            // 如果更新失敗，回退點贊狀態和數字
            console.error("Error updating like status:", error);
            likeIcon.classList.toggle("liked", isLiked); // 回退到原始狀態
            likeCountElement.textContent = isLiked
              ? likeCount + 1
              : likeCount - 1; // 回退數字
          });
        } else {
          console.error("accountId or postId is missing");
        }
      }
    });
}

async function fetchUpdateLike(accountId, postId, likePostData) {
  const token = localStorage.getItem("userToken");

  const likePostURL = `/api/member/${encodeURIComponent(
    accountId
  )}/post/${encodeURIComponent(postId)}/like`;

  try {
    const response = await fetch(likePostURL, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(likePostData),
    });

    console.log("body:", JSON.stringify(likePostData));

    if (!response.ok) {
      console.log("Failed to like post:", response.message);

      throw new Error(`HTTP status ${response.status}`);
    }
  } catch (error) {
    console.error("Error updating like the post", error);
  } finally {
  }
}

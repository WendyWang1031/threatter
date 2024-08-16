export function selectSinglePost() {
  document
    .querySelector(".postsContainer")
    .addEventListener("click", (event) => {
      // 確認點擊的元素或其父元素是否是 .post
      event.preventDefault(); // 阻止默認行為

      // const post_header = event.target.closest(".post-header");
      const post_content = event.target.closest(".post-content");

      // 檢查是否點擊了 menu-button 或其子元素
      const menuButton = event.target.closest(".menu-button");

      if (menuButton) {
        return; // 直接返回，不進行後續處理
      }

      const memberPage = document.querySelector(".account_id");
      if (memberPage) {
        event.preventDefault(); // 阻止默認行為
        const postElement = event.target.closest(".post");
        const accountIdElement = postElement.querySelector(".account_id");
        const accountId = accountIdElement.textContent.trim();
        const targetUrl = `/member/${encodeURIComponent(accountId)}`;
        window.location.href = targetUrl;
      }

      if (post_content) {
        console.log("Post clicked via delegation:", post_content);
        event.preventDefault(); // 阻止默認行為

        // 獲取 account_id 和 post_id
        const postElement = event.target.closest(".post");
        const accountIdElement = postElement.querySelector(".account_id");
        const postIdElement = postElement.querySelector(".post_id");

        if (accountIdElement && postIdElement) {
          const accountId = accountIdElement.textContent.trim();
          const postId = postIdElement.textContent.trim();
          const targetUrl = `/member/${encodeURIComponent(
            accountId
          )}/post/${encodeURIComponent(postId)}`;
          console.log("Navigating to:", targetUrl);
          window.location.href = targetUrl;
        } else {
          console.error("accountId or postId is missing");
        }
      }
    });
}

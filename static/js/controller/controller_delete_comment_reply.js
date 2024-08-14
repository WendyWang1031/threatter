export async function deleteComment() {
  document
    .querySelector(".single-CommentContainer")
    .addEventListener("click", async (event) => {
      if (event.target.id.includes("delete-comment")) {
        const commentElement = event.target.closest(".message");
        const commentIdElement = commentElement.querySelector(".message_id");
        const token = localStorage.getItem("userToken");

        if (commentElement && commentIdElement) {
          // 獲取該貼文的 主人 和  post_id
          const currentUrl = window.location.pathname;
          const pathSegments = currentUrl.split("/"); // 以 "/" 分割路徑成為陣列
          const accountId = pathSegments[2]; // 第三個元素為 account_id
          const postId = pathSegments[4]; // 第五個元素為 post_id

          const postElement = event.target.closest(".post");
          const commentIdElement = postElement.querySelector(".message_id");
          const commentId = commentIdElement.textContent.trim();

          console.log("accountId:", accountId);
          console.log("postId:", postId);
          console.log("commentId:", commentId);

          try {
            const response = await fetch(
              `/api/member/${accountId}/post/${postId}/comment/${commentId}/reply`,
              {
                method: "DELETE",
                headers: {
                  Authorization: `Bearer ${token}`,
                },
              }
            );

            if (response.ok) {
              window.location.reload();
            } else {
              alert("刪除留言失敗，請排查問題。");
            }
          } catch (error) {
            console.error("刪除留言失敗:", error);
          }
        }
      }
    });
}

export async function deleteReply() {
  document
    .querySelector(".single-CommentContainer")
    .addEventListener("click", async (event) => {
      if (event.target.id.includes("delete-reply")) {
        const replyarea = event.target.closest(".reply-area");
        const replycontent = replyarea.querySelector(".reply-content");

        const token = localStorage.getItem("userToken");

        if (replyarea && replycontent) {
          // 獲取該貼文的 主人 和  post_id
          const currentUrl = window.location.pathname;
          const pathSegments = currentUrl.split("/"); // 以 "/" 分割路徑成為陣列
          const accountId = pathSegments[2]; // 第三個元素為 account_id
          const postId = pathSegments[4]; // 第五個元素為 post_id

          const replyIdElement = replycontent.querySelector(".reply_id");

          const replyId = replyIdElement.textContent.trim();

          console.log("accountId:", accountId);
          console.log("postId:", postId);
          console.log("reply_id:", replyId);

          try {
            const response = await fetch(
              `/api/member/${accountId}/post/${postId}/comment/${replyId}/reply`,
              {
                method: "DELETE",
                headers: {
                  Authorization: `Bearer ${token}`,
                },
              }
            );

            if (response.ok) {
              window.location.reload();
            } else {
              alert("刪除留言失敗，請排查問題。");
            }
          } catch (error) {
            console.error("刪除留言失敗:", error);
          }
        }
      }
    });
}

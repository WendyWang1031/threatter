import {
  fetchMemberDetail,
  editMember,
  uploadAvatar,
} from "./controller/controller_member.js";
import { closeEditMember } from "./view/view_member.js";
import { PermissionAllIcon } from "./view/view_icon.js";
import { displayContentElement, displayMenuBtn } from "./view/view_posts.js";
import { likePost } from "./controller/controller_like.js";

document.addEventListener("DOMContentLoaded", async function () {
  PermissionAllIcon();
  closeEditMember();
  fetchMemberDetail();
  fetchGetPost();
  displayMenuBtn();

  uploadAvatar();

  likePost();

  const OutsideMemberBtn = document.querySelector(".edit-profile-button");
  OutsideMemberBtn.addEventListener("click", editMember);
});

let currentPage = 0;
let hasNextPage = true;
let isWaitingForData = false;

const observer = new IntersectionObserver(
  (entries) => {
    const firstEntry = entries[0];

    if (firstEntry.isIntersecting && hasNextPage && !isWaitingForData) {
      //調用fetch函式的時候使用非同步加載
      fetchGetPost();
    }
  },
  { threshold: 0.5 }
);

async function fetchGetPost() {
  const currentUrl = window.location.pathname;
  const urlAccountId = currentUrl.split("/").pop();

  // 抓取當前用戶
  const localAccountId = localStorage.getItem("account_id");

  // 判斷是否當前用戶
  const isCurrentUser = urlAccountId === localAccountId;
  const account_id = isCurrentUser ? localAccountId : urlAccountId;

  if (!account_id) {
    console.log("User not logged in, using default avatar.");
    return;
  }

  const memberPostsUrl = `/api/member/${encodeURIComponent(
    account_id
  )}/posts?page=${currentPage}`;

  try {
    //開始新的資料加載前設定
    isWaitingForData = true;
    const response = await fetch(memberPostsUrl);
    const result = await response.json();

    let lastItem = document.querySelector(".indivisial-area:last-child");
    if (result && result.data.length > 0) {
      currentPage++;
      hasNextPage = result.next_page != null;

      const postsContainer = document.querySelector(".postsContainer");
      result.data.forEach((post) => {
        const postElement = displayContentElement(post);
        postsContainer.appendChild(postElement);
      });

      let newItem = document.querySelector(".indivisial-area:last-child");
      if (lastItem) observer.unobserve(lastItem);
      if (hasNextPage) {
        if (newItem) observer.observe(newItem);
      }
    } else {
      hasNextPage = false;
    }
    isWaitingForData = false;
  } catch (error) {
    console.error("Error fetching post data:", error);
    isWaitingForData = false;
  }
}

import {
  fetchMemberDetail,
  editMember,
  uploadAvatar,
} from "./controller/controller_member.js";
import { closeEditMember } from "./view/view_member.js";
import {
  displayOrCloseFansAndFollow,
  displayUpdateFollowerCount,
} from "./view/view_fans_follower.js";
import { PermissionAllIcon } from "./view/view_icon.js";
import { displayContentElement, displayMenuBtn } from "./view/view_posts.js";
import { likePost } from "./controller/controller_like.js";
import { selectSinglePost } from "./controller/controller_select_single_post.js";
import {
  fetchAndDisplayFans,
  fetchAndDisplayFollowers,
  setupIntersectionObserverFansAndFollow,
} from "./controller/controller_fans_follower.js";
import { stringifyObjectValues } from "./controller/controller_convert_to_string.js";

document.addEventListener("DOMContentLoaded", async function () {
  PermissionAllIcon();
  closeEditMember();
  fetchMemberDetail();
  fetchGetPost();
  displayMenuBtn();

  uploadAvatar();

  setupIntersectionObserver();
  setupTabSwitching();
  displayUpdateFollowerCount();

  likePost();
  selectSinglePost();

  const fansListContainer = document.querySelector(".fans-list");
  const followListContainer = document.querySelector(".follow-list");

  await fetchAndDisplayFans(fansListContainer);
  await fetchAndDisplayFollowers(followListContainer);

  setupIntersectionObserverFansAndFollow(
    fansListContainer,
    followListContainer
  );

  const fans_follow_list = document.querySelector(".user-fans");
  fans_follow_list.addEventListener("click", displayOrCloseFansAndFollow);

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

  const token = localStorage.getItem("userToken");
  const headers = token ? { Authorization: `Bearer ${token}` } : {};

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
    const response = await fetch(memberPostsUrl, {
      headers: headers,
    });
    let result = await response.json();
    result = stringifyObjectValues(result);
    const postsContainer = document.querySelector(".postsContainer");

    const noData = document.createElement("div");
    noData.className = "no-data";
    const noDataMessage = document.createElement("div");
    noDataMessage.className = "no-data-message";

    let lastItem = document.querySelector(".indivisial-area:last-child");

    if (
      result.message ===
      "FAILED to get member's posts data or have no permission"
    ) {
      noDataMessage.textContent = "尚無任何串文。";

      noData.appendChild(noDataMessage);
      postsContainer.appendChild(noData);
    } else if (result.message === "User not authenticated") {
      noDataMessage.textContent = "此個人檔案不公開。";

      noData.appendChild(noDataMessage);
      postsContainer.appendChild(noData);

      const userFansLink = document.querySelector(".user-fans");
      if (userFansLink) {
        userFansLink.removeAttribute("href");
        userFansLink.style.pointerEvents = "none";
        userFansLink.style.color = "gray";
      }
    }

    if (result && result.data.length > 0) {
      currentPage++;
      hasNextPage = result.next_page != null;

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

      // const memberSelfArea = document.querySelector(".member-self-area");
      // const noDataMessage = document.createElement("div");
      // noDataMessage.className = "no-data-message";
      // noDataMessage.textContent = "此個人檔案不公開。";
      // memberSelfArea.appendChild(noDataMessage);
    }
    isWaitingForData = false;
  } catch (error) {
    console.error("Error fetching post data:", error);
    isWaitingForData = false;
  }
}

function setupTabSwitching() {
  const tabs = document.querySelectorAll(".follower-header .tab");
  const followerLists = {
    fans: document.querySelector(".fans-list"),
    follow: document.querySelector(".follow-list"),
  };

  tabs.forEach((tab) => {
    tab.addEventListener("click", async function () {
      tabs.forEach((t) => t.classList.remove("active"));
      this.classList.add("active");

      Object.values(followerLists).forEach(
        (list) => (list.style.display = "none")
      );

      const targetListClass = this.getAttribute("data-target");
      const targetList = document.querySelector(`.${targetListClass}`);

      if (targetListClass === "fans-list") {
        await fetchAndDisplayFans(targetList);
      } else if (targetListClass === "follow-list") {
        await fetchAndDisplayFollowers(targetList);
      }

      targetList.style.display = "block";
    });
  });
}

function setupIntersectionObserver() {
  const fansListContainer = document.querySelector(".fans-list");
  const followListContainer = document.querySelector(".follow-list");
  const observer = new IntersectionObserver(async (entries, observer) => {
    const [entry] = entries;
    if (entry.isIntersecting) {
      await fetchAndDisplayFans(fansListContainer);
      await fetchAndDisplayFollowers(followListContainer);
      observer.disconnect();
    }
  });

  observer.observe(fansListContainer);
  observer.observe(followListContainer);
}

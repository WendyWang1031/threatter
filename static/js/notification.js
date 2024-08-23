import { PermissionAllIcon } from "./view/view_icon.js";
import {
  displayFollowerItem,
  displayNotificationItem,
} from "./view/view_notification.js";
import { markAllNotificationsAsRead } from "./controller/controller_notification.js";

// import //   setupIntersectionObserver,
// "./controller/controller_notification.js";

document.addEventListener("DOMContentLoaded", async function () {
  PermissionAllIcon();
  setupTabSwitching();

  //   setupIntersectionObserver();

  markAllNotificationsAsRead();
});

let currentPage = 0;
let hasNextPage = true;
let isWaitingForData = false;

const observer = new IntersectionObserver(
  (entries) => {
    const firstEntry = entries[0];

    if (firstEntry.isIntersecting && hasNextPage && !isWaitingForData) {
      //調用fetch函式的時候使用非同步加載
      const targetList = document.querySelector(".notify-req-list.active");
      if (targetList) {
        fetchAndDisplayFollowReq(targetList);
      }
    }
  },
  { threshold: 0.5 }
);

export function setupTabSwitching() {
  console.log("here");
  const tabs = document.querySelectorAll(".nav-button");
  const notifyLists = {
    notifyReq: document.querySelector(".notify-req-list"),
    notifyAni: document.querySelector(".notify-ani-list"),
  };

  tabs.forEach((tab) => {
    tab.addEventListener("click", async function () {
      // 移除所有標籤的 active
      tabs.forEach((t) => t.classList.remove("active"));
      // 添加 active
      this.classList.add("active");

      // 隱藏
      Object.values(notifyLists).forEach((list) => {
        list.style.display = "none";
        list.classList.remove("active");
      });

      const targetListClass = this.getAttribute("data-target");
      const targetList = document.querySelector(`.${targetListClass}`);
      targetList.style.display = "block";
      targetList.classList.add("active");

      if (targetListClass === "notify-req-list") {
        await fetchAndDisplayFollowReq(targetList);
      } else if (targetListClass === "notify-ani-list") {
        await fetchAndDisplayNotification(targetList);
      }
    });
  });
}

async function fetchAndDisplayFollowReq(targetList) {
  const token = localStorage.getItem("userToken");

  try {
    isWaitingForData = true;
    // const response = await fetch(
    //     `/api/member/${urlAccountId}/follow/fans?page=${currentPage}`,
    //     {
    //       headers: headers,
    //     }
    //   );
    const response = await fetch(
      `/api/follow/member/follow?page=${currentPage}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      }
    );
    const followReqData = await response.json();
    console.log("followReqData:", followReqData);

    // targetList.innerHTML = "";

    let lastItem = document.querySelector(".list-item:last-child");
    if (followReqData.data && followReqData.data.length > 0) {
      currentPage++;
      hasNextPage = followReqData.next_page != null;

      followReqData.data.forEach((followerReq) => {
        const fanItem = displayFollowerItem(followerReq);
        targetList.appendChild(fanItem);
      });

      let newItem = document.querySelector(".list-item:last-child");
      if (lastItem) observer.unobserve(lastItem);
      if (hasNextPage) {
        if (newItem) observer.observe(newItem);
      }
    } else {
      hasNextPage = false;
      const noDataMessage = document.createElement("div");
      noDataMessage.className = "no-data-message";
      noDataMessage.textContent = "目前尚無要求追蹤的對象清單";
      targetList.appendChild(noDataMessage);
    }

    targetList.style.display = "block";
    isWaitingForData = false;
  } catch (error) {
    console.error("Error fetching follower Request:", error);
    isWaitingForData = false;
  } finally {
  }
}

async function fetchAndDisplayNotification(targetList) {
  const token = localStorage.getItem("userToken");

  try {
    isWaitingForData = true;

    const response = await fetch(`/api/notification?page=${currentPage}`, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });
    const notifyData = await response.json();
    console.log("notifyData:", notifyData);

    targetList.innerHTML = "";

    let lastItem = document.querySelector(".list-item:last-child");
    if (notifyData.data && notifyData.data.length > 0) {
      currentPage++;
      hasNextPage = notifyData.next_page != null;

      notifyData.data.forEach((notification) => {
        const notifyItem = displayNotificationItem(notification);
        targetList.appendChild(notifyItem);
      });

      let newItem = document.querySelector(".list-item:last-child");
      if (lastItem) observer.unobserve(lastItem);
      if (hasNextPage) {
        if (newItem) observer.observe(newItem);
      }
    }

    targetList.style.display = "block";
    isWaitingForData = false;
  } catch (error) {
    console.error("Error fetching notifications:", error);
    isWaitingForData = false;
  } finally {
  }
}

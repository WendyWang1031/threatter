import { PermissionAllIcon } from "./view/view_icon.js";
import {
  displayFollowerItem,
  displayNotificationItem,
} from "./view/view_notification.js";
import { markAllNotificationsAsRead } from "./controller/controller_notification.js";
import { stringifyObjectValues } from "./controller/controller_convert_to_string.js";

document.addEventListener("DOMContentLoaded", async function () {
  PermissionAllIcon();
  setupTabSwitching();

  createObserver();

  markAllNotificationsAsRead();

  const defaultTab = document.querySelector(".nav-button.active");
  if (defaultTab) {
    defaultTab.click();
  }
});

let currentPageReq = 0;
let currentPageAni = 0;
let hasNextPageReq = true;
let hasNextPageAni = true;
let isWaitingForDataReq = false;
let isWaitingForDataAni = false;

let observerReq;
let observerAni;

function createObserver(targetList, fetchFunction) {
  return new IntersectionObserver(
    (entries) => {
      const firstEntry = entries[0];
      if (
        firstEntry.isIntersecting &&
        !isWaitingForDataReq &&
        !isWaitingForDataAni
      ) {
        fetchFunction(targetList);
      }
    },
    { threshold: 0.5 }
  );
}

function removeNoDataMessage(targetList) {
  const noDataMessage = targetList.querySelector(".no-data-message");
  if (noDataMessage) {
    noDataMessage.remove();
  }
}

export function setupTabSwitching() {
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

      // 取消之前的觀察
      if (observerReq) observerReq.disconnect();
      if (observerAni) observerAni.disconnect();

      removeNoDataMessage(targetList);

      if (targetListClass === "notify-req-list") {
        observerReq = createObserver(targetList, fetchAndDisplayFollowReq);
        await fetchAndDisplayFollowReq(targetList);
      } else if (targetListClass === "notify-ani-list") {
        observerAni = createObserver(targetList, fetchAndDisplayNotification);
        await fetchAndDisplayNotification(targetList);
      }
    });
  });
}

async function fetchAndDisplayFollowReq(targetList) {
  const token = localStorage.getItem("userToken");

  try {
    isWaitingForDataReq = true;

    const response = await fetch(
      `/api/follow/member/follow?page=${currentPageReq}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      }
    );
    let followReqData = await response.json();
    console.log("followReqData:", followReqData);
    followReqData = stringifyObjectValues(followReqData);

    // targetList.innerHTML = "";

    let lastItem = document.querySelector(".list-item:last-child");
    if (followReqData.data && followReqData.data.length > 0) {
      currentPageReq++;
      hasNextPageReq = followReqData.next_page != null;

      followReqData.data.forEach((followerReq) => {
        const fanItem = displayFollowerItem(followerReq);
        targetList.appendChild(fanItem);
      });

      let newItem = document.querySelector(".list-item:last-child");
      if (lastItem && observerReq) observerReq.unobserve(lastItem);
      if (hasNextPageReq && newItem && observerReq) {
        observerReq.observe(newItem);
      }
    } else if (currentPageReq === 0) {
      hasNextPageReq = false;
      const noDataMessage = document.createElement("div");
      noDataMessage.className = "no-data-message";
      noDataMessage.textContent = "目前尚無要求追蹤的對象清單";
      targetList.appendChild(noDataMessage);
    }

    targetList.style.display = "block";
    isWaitingForDataReq = false;
  } catch (error) {
    console.error("Error fetching follower Request:", error);
    isWaitingForDataReq = false;
  } finally {
  }
}

async function fetchAndDisplayNotification(targetList) {
  const token = localStorage.getItem("userToken");

  try {
    isWaitingForDataAni = true;

    const response = await fetch(`/api/notification?page=${currentPageAni}`, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });
    let notifyData = await response.json();
    console.log("notifyData:", notifyData);
    notifyData = stringifyObjectValues(notifyData);

    // targetList.innerHTML = "";

    let lastItem = document.querySelector(".like indivisual-list:last-child");
    if (notifyData.data && notifyData.data.length > 0) {
      currentPageAni++;
      hasNextPageAni = notifyData.next_page != null;

      notifyData.data.forEach((notification) => {
        const notifyItem = displayNotificationItem(notification);
        targetList.appendChild(notifyItem);
      });

      let newItem = document.querySelector(".like.indivisual-list:last-child");
      if (lastItem) observerAni.unobserve(lastItem);
      if (hasNextPageAni && newItem) {
        observerAni.observe(newItem);
      }
    } else if (currentPageAni === 0) {
      hasNextPageAni = false;
      const noDataMessage = document.createElement("div");
      noDataMessage.className = "no-data-message";
      noDataMessage.textContent = "目前尚無動態通知";
      targetList.appendChild(noDataMessage);
    }

    targetList.style.display = "block";
    isWaitingForDataAni = false;
  } catch (error) {
    console.error("Error fetching notifications:", error);
    isWaitingForDataAni = false;
  } finally {
  }
}

import { displayFollowerItem } from "../view/view_notification.js";

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
        //   } else if (targetListClass === "notify-ani-list") {
        //     await fetchAndDisplayFollowAni(targetList);
      }
    });
  });
}

export async function fetchAndDisplayFollowReq(targetList) {
  const token = localStorage.getItem("userToken");

  try {
    // const response = await fetch(
    //     `/api/member/${urlAccountId}/follow/fans?page=${currentPage}`,
    //     {
    //       headers: headers,
    //     }
    //   );
    const response = await fetch(`/api/follow/member/follow`, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });
    const followReqData = await response.json();
    console.log("followReqData:", followReqData);

    targetList.innerHTML = "";

    if (followReqData.data && followReqData.data.length > 0) {
      followReqData.data.forEach((followerReq) => {
        const fanItem = displayFollowerItem(followerReq);
        targetList.appendChild(fanItem);
      });
    } else {
      const noDataMessage = document.createElement("div");
      noDataMessage.className = "no-data-message";
      noDataMessage.textContent = "目前尚無 要求追蹤 的對象清單";
      targetList.appendChild(noDataMessage);
    }

    targetList.style.display = "block";
  } catch (error) {
    console.error("Error fetching follower Request:", error);
  } finally {
  }
}

export function setupIntersectionObserver() {
  const followerReqListContainer = document.querySelector(".notify-req-list");

  const observer = new IntersectionObserver(async (entries, observer) => {
    const [entry] = entries;
    if (entry.isIntersecting) {
      await fetchAndDisplayFollowReq(followerReqListContainer);

      observer.disconnect();
    }
  });

  observer.observe(followerReqListContainer);
}

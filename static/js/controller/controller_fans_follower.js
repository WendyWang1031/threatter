import {
  displayFollowerItem,
  displayUpdateFollowerCount,
} from "../view/view_fans_follower.js";

let currentPageFans = 0;
let hasNextPageFans = true;
let isWaitingForDataFans = false;

let currentPageFollow = 0;
let hasNextPageFollow = true;
let isWaitingForDataFollow = false;

export function setupIntersectionObserverFansAndFollow(
  fansListContainer,
  followListContainer
) {
  const observer = new IntersectionObserver(async (entries, observer) => {
    const [entry] = entries;
    if (entry.isIntersecting) {
      if (fansListContainer.contains(entry.target)) {
        await fetchAndDisplayFans(fansListContainer);
      } else if (followListContainer.contains(entry.target)) {
        await fetchAndDisplayFollowers(followListContainer);
      }

      observer.unobserve(entry.target);
    }
  });

  observer.observe(fansListContainer);
  observer.observe(followListContainer);
}

export async function fetchAndDisplayFans(targetList) {
  if (!hasNextPageFans || isWaitingForDataFans) return;

  const token = localStorage.getItem("userToken");
  const headers = token ? { Authorization: `Bearer ${token}` } : {};

  const currentUrl = window.location.pathname;
  const urlAccountId = currentUrl.split("/").pop();

  isWaitingForDataFans = true;

  try {
    // const response = await fetch(
    //     `/api/member/${urlAccountId}/follow/fans?page=${currentPage}`,
    //     {
    //       headers: headers,
    //     }
    //   );
    const response = await fetch(`/api/member/${urlAccountId}/follow/fans`, {
      headers: headers,
    });
    const result = await response.json();

    if (result.data && result.data.length > 0) {
      currentPageFans++;
      hasNextPageFans = result.next_page != null;

      result.data.forEach((fan) => {
        const fanItem = displayFollowerItem(fan);
        targetList.appendChild(fanItem);
      });

      let newItem = document.querySelector(".list-item:last-child");
      if (newItem && hasNextPageFans) observer.observe(newItem);
    } else {
      hasNextPageFans = false;
      if (currentPageFans === 0) {
        const noData = document.createElement("div");
        noData.className = "no-data";
        const noDataMessage = document.createElement("div");
        noDataMessage.className = "no-data-message";
        noDataMessage.textContent = "目前尚無粉絲";
        noData.appendChild(noDataMessage);
        targetList.appendChild(noData);
      }
    }
  } catch (error) {
    console.error("Error fetching fans:", error);
  } finally {
    isWaitingForDataFans = false;
  }
}

export async function fetchAndDisplayFollowers(targetList) {
  if (!hasNextPageFollow || isWaitingForDataFollow) return;

  const token = localStorage.getItem("userToken");
  const headers = token ? { Authorization: `Bearer ${token}` } : {};

  const currentUrl = window.location.pathname;
  const urlAccountId = currentUrl.split("/").pop();

  isWaitingForDataFollow = true;

  try {
    const response = await fetch(`/api/member/${urlAccountId}/follow/target`, {
      headers: headers,
    });
    const result = await response.json();

    if (result.data && result.data.length > 0) {
      currentPageFollow++;
      hasNextPageFollow = result.next_page != null;

      result.data.forEach((follower) => {
        const followerItem = displayFollowerItem(follower);
        targetList.appendChild(followerItem);
      });

      let newItem = document.querySelector(".list-item:last-child");
      if (newItem && hasNextPageFollow) observer.observe(newItem);
    } else {
      hasNextPageFollow = false;
      if (currentPageFollow === 0) {
        const noData = document.createElement("div");
        noData.className = "no-data";
        const noDataMessage = document.createElement("div");
        noDataMessage.className = "no-data-message";
        noDataMessage.textContent = "目前尚無追蹤的對象";
        noData.appendChild(noDataMessage);
        targetList.appendChild(noData);
      }
    }
  } catch (error) {
    console.error("Error fetching followers:", error);
  } finally {
    isWaitingForDataFollow = false;
  }
}

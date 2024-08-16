import { PermissionAllIcon } from "./view/view_icon.js";
import { displayFollowerItem } from "./view/view_search.js";

// import //   setupIntersectionObserver,
// "./controller/controller_notification.js";

document.addEventListener("DOMContentLoaded", async function () {
  PermissionAllIcon();

  const searchInput = document.getElementById("search-input");

  searchInput.addEventListener(
    "input",
    debounce(function () {
      currentPage = 0;
      fetchAndDisplaySearch(this.value.trim());
    }, 300)
  );
});

let currentPage = 0;
let hasNextPage = true;
let isWaitingForData = false;

const observer = new IntersectionObserver(
  (entries) => {
    const firstEntry = entries[0];

    if (firstEntry.isIntersecting && hasNextPage && !isWaitingForData) {
      //調用fetch函式的時候使用非同步加載

      fetchAndDisplaySearch();
    }
  },
  { threshold: 0.5 }
);

function debounce(func, delay) {
  let timeout;
  return function (...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), delay);
  };
}

async function fetchAndDisplaySearch(query) {
  const userToken = localStorage.getItem("userToken");
  const headers = userToken ? { Authorization: `Bearer ${userToken}` } : {};

  try {
    isWaitingForData = true;

    const response = await fetch(
      `/api/search?search=${encodeURIComponent(query)}&page=${currentPage}`,
      {
        headers: headers,
      }
    );
    const result = await response.json();

    const targetList = document.querySelector(".search-list");
    if (currentPage === 0) {
      targetList.innerHTML = "";
    }

    let lastItem = document.querySelector(".list-item:last-child");
    if (result.data && result.data.length > 0) {
      currentPage++;
      hasNextPage = result.next_page != null;

      result.data.forEach((followerReq) => {
        const fanItem = displayFollowerItem(followerReq);
        targetList.appendChild(fanItem);
      });

      let newItem = document.querySelector(".list-item:last-child");
      if (lastItem) observer.unobserve(lastItem);
      if (hasNextPage) {
        if (newItem) observer.observe(newItem);
      }
    } else if (currentPage === 0) {
      const noDataMessage = document.createElement("div");
      noDataMessage.className = "no-data-message";
      noDataMessage.textContent = "目前尚無搜尋結果";
      targetList.appendChild(noDataMessage);
    }

    targetList.style.display = "block";
    isWaitingForData = false;
  } catch (error) {
    console.error("Error searching:", error);
    isWaitingForData = false;
  } finally {
  }
}

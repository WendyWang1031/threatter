export function displayOrCloseFansAndFollow() {
  const fans_follow_container = document.querySelector(".fans-follow");
  fans_follow_container.style.display = "flex";

  // 點擊遮罩地方可以關閉
  fans_follow_container.addEventListener("click", function (event) {
    if (event.target === fans_follow_container) {
      closeModal();
    }
  });

  // 關閉
  function closeModal() {
    fans_follow_container.style.display = "none";
  }
}

export function setupTabSwitching() {
  const tabs = document.querySelectorAll(".follower-header .tab");
  const followerLists = {
    fans: document.querySelector(".fans-list"),
    follow: document.querySelector(".follow-list"),
  };

  tabs.forEach((tab) => {
    tab.addEventListener("click", async function () {
      // 移除所有標籤的 active
      tabs.forEach((t) => t.classList.remove("active"));
      // 添加 active
      this.classList.add("active");

      // 隱藏
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
    });
  });
}

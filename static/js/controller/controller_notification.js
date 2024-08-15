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

      //   if (targetListClass === "notify-req-list") {
      //     await fetchAndDisplayFans(targetList);
      //   } else if (targetListClass === "notify-ani-list") {
      //     await fetchAndDisplayFollowers(targetList);
      //   }
    });
  });
}

import {
  displayFollowerItem,
  displayUpdateFollowerCount,
} from "../view/view_fans_follower.js";

export async function fetchAndDisplayFans(targetList) {
  const token = localStorage.getItem("userToken");
  const headers = token ? { Authorization: `Bearer ${token}` } : {};

  const currentUrl = window.location.pathname;
  const urlAccountId = currentUrl.split("/").pop();

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
    const fansData = await response.json();

    targetList.innerHTML = "";

    fansData.data.forEach((fan) => {
      const fanItem = displayFollowerItem(fan);
      targetList.appendChild(fanItem);
    });

    displayUpdateFollowerCount("fans-list", fansData.fans_counts);

    targetList.style.display = "block";
  } catch (error) {
    console.error("Error fetching fans:", error);
  } finally {
  }
}

export async function fetchAndDisplayFollowers(targetList) {
  const token = localStorage.getItem("userToken");
  const headers = token ? { Authorization: `Bearer ${token}` } : {};

  const currentUrl = window.location.pathname;
  const urlAccountId = currentUrl.split("/").pop();

  try {
    const response = await fetch(`/api/member/${urlAccountId}/follow/target`, {
      headers: headers,
    });
    const followersData = await response.json();
    console.log("followersData:", followersData);

    targetList.innerHTML = "";

    followersData.data.forEach((follower) => {
      const followerItem = displayFollowerItem(follower);
      targetList.appendChild(followerItem);
    });

    displayUpdateFollowerCount("follow-list", followersData.fans_counts);

    targetList.style.display = "block";
  } catch (error) {
    console.error("Error fetching followers:", error);
  } finally {
  }
}

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

export async function markAllNotificationsAsRead() {
  const token = localStorage.getItem("userToken");
  const currentTime = new Date().toISOString();

  const requestBody = { current_time: currentTime };

  const response = await fetch("/api/notification/mark_all_read", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(requestBody),
  });

  if (response.ok) {
    console.log("All notifications marked as read.");
  } else {
    console.error("Failed to mark notifications as read.");
  }
}

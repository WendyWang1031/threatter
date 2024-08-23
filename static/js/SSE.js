document.addEventListener("DOMContentLoaded", async function () {
  SSE();
  checkNotifications();
});

async function SSE() {
  const token = localStorage.getItem("userToken");

  if (!token) {
    console.error("Token not found in localStorage");
    return;
  }

  const eventSource = new EventSource(
    `/api/notification/stream?token=${token}`,
    {
      withCredentials: true,
    }
  );

  eventSource.onmessage = function (event) {
    console.log("New notification:", event.data);
    console.log("EventSource state:", eventSource.readyState);

    const notificationDot = document.querySelector(".notification-dot");
    notificationDot.style.display = "block";
  };

  eventSource.onerror = function (event) {
    console.error("EventSource failed:", event);
    console.log("EventSource state:", eventSource.readyState);
  };
}

async function checkNotifications() {
  const token = localStorage.getItem("userToken");

  if (!token) {
    console.error("Token not found in localStorage");
    return;
  }

  try {
    const response = await fetch("/api/notification?page=0", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });

    if (response.ok) {
      const data = await response.json();

      // 檢查是否有未讀的通知
      const hasUnreadNotifications = data.data.some(
        (notification) => !notification.is_read
      );

      if (hasUnreadNotifications) {
        // 如果有，就是顯示紅點
        const notificationDot = document.querySelector(".notification-dot");
        notificationDot.style.display = "block";
      }
    } else {
      console.error("Failed to fetch notifications");
    }
  } catch (error) {
    console.error("Error:", error);
  }
}

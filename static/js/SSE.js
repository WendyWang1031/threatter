document.addEventListener("DOMContentLoaded", async function () {
  SSE();
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

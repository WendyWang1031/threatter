document.addEventListener("DOMContentLoaded", async function () {
  // SSE();
  initializeSSE();
  checkNotifications();
});

window.addEventListener("beforeunload", () => {
  if (sseWorker) {
    sseWorker.postMessage("close");
    sseWorker.terminate();
    localStorage.removeItem("sseWorkerInitialized");
  }
});

let sseWorker;

async function initializeSSE() {
  if (window.Worker) {
    // 檢查是否已經有一個 Worker 運行
    if (!sseWorker) {
      const workerScript = `
        self.onmessage = function (event) {
          const { token, sseUrl } = event.data;
          
          const baseUrl = location.origin;
          const encodedToken = encodeURIComponent(token);
          const eventSource = new EventSource(\`\${baseUrl}\${sseUrl}?token=\${encodedToken}\`);

          eventSource.onmessage = function (e) {
            self.postMessage({ type: "new-notification", data: e.data });
          };

          eventSource.onerror = function (err) {
            console.error("SSE error in worker:", err);
            self.postMessage({ type: "error", data: err });
          };

         
          self.onmessage = function(e) {
            if (e.data === "close") {
              eventSource.close();
            }
          };
        };
      `;

      const blob = new Blob([workerScript], { type: "application/javascript" });
      const workerUrl = URL.createObjectURL(blob);

      sseWorker = new Worker(workerUrl);
      const token = localStorage.getItem("userToken");

      if (!token) {
        console.error("Token not found in localStorage");
        return;
      }

      // 傳送 Token 和 SSE 的 URL 給 Worker
      sseWorker.postMessage({
        token: token,
        sseUrl: "/api/notification/stream",
      });

      sseWorker.onmessage = function (event) {
        const { type, data } = event.data;

        if (type === "new-notification") {
          console.log("New notification:", data);
          const notificationDot = document.querySelector(".notification-dot");
          if (notificationDot) {
            notificationDot.style.display = "block";
          }
        } else if (type === "error") {
          console.error("SSE error:", data);
        }
      };

      // 儲存狀態到 localStorage 以便其他頁面能知道 Worker 已經啟動
      localStorage.setItem("sseWorkerInitialized", "true");
    }
  } else {
    console.error("Web Workers are not supported in this browser.");
  }
}

// async function SSE() {
//   const token = localStorage.getItem("userToken");

//   if (!token) {
//     console.error("Token not found in localStorage");
//     return;
//   }

//   const eventSource = new EventSource(
//     `/api/notification/stream?token=${token}`,
//     {
//       withCredentials: true,
//     }
//   );

//   eventSource.onmessage = function (event) {
//     console.log("New notification:", event.data);
//     console.log("EventSource state:", eventSource.readyState);

//     const notificationDot = document.querySelector(".notification-dot");
//     notificationDot.style.display = "block";
//   };

//   eventSource.onerror = function (event) {
//     console.error("EventSource failed:", event);
//     console.log("EventSource state:", eventSource.readyState);
//   };
// }

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

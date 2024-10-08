export function PermissionAllIcon() {
  const logo = document.querySelector(".logo");
  const homeLogo = document.querySelector(".home");
  logo.addEventListener("click", function () {
    window.location.href = "/";
  });
  homeLogo.addEventListener("click", function () {
    window.location.href = "/";
  });

  const token = localStorage.getItem("userToken");

  const notify = document.querySelector(".heart");
  const search = document.querySelector(".search");
  const profile = document.querySelector(".profile");

  const signin_mask = document.querySelector(".signin-mask");

  if (!token) {
    notify.addEventListener("click", function () {
      signin_mask.style.display = "flex";
    });
    profile.addEventListener("click", function () {
      signin_mask.style.display = "flex";
    });
    search.addEventListener("click", function () {
      signin_mask.style.display = "flex";
    });
  } else {
    profile.addEventListener("click", function () {
      const account_id = localStorage.getItem("account_id");
      const memberUrl = `/member/${encodeURIComponent(account_id)}`;
      window.location.href = memberUrl;
    });

    notify.addEventListener("click", function () {
      const notifyUrl = "/notification";
      window.location.href = notifyUrl;
    });

    search.addEventListener("click", function () {
      const searchUrl = "/search";
      window.location.href = searchUrl;
    });
  }
}

import * as Model from "../model/auth.js";
import * as View from "../view/view.js";
import { stringifyObjectValues } from "./controller_convert_to_string.js";

const userRegisterUrl = "/api/user";
const userSignInUrl = "/api/user/auth";

export function setupEventListeners() {
  document
    .querySelector(".login-signin")
    .addEventListener("click", () =>
      View.setElementDisplay(".signin-mask", "flex")
    );

  //測試帳號
  document.querySelector(".quick-login").addEventListener("click", async () => {
    const testAccount = "test_user";
    const testPassword = "test_password";

    document.getElementById("signin-account-id").value = testAccount;
    document.getElementById("signin-password").value = testPassword;

    const event = new Event("submit");
    document.querySelector(".signin").dispatchEvent(event);
  });

  document.querySelector(".go-to-signup").addEventListener("click", () => {
    View.setElementDisplay(".signin-mask", "none");
    View.setElementDisplay(".signup-mask", "flex");
    View.setElementDisplay(".hint-signin-message", "none");
    View.clearInputs("signin-account-id", "signin-password");
  });

  document.querySelector(".go-to-signin").addEventListener("click", () => {
    View.setElementDisplay(".signup-mask", "none");
    View.setElementDisplay(".signin-mask", "flex");
    View.setElementDisplay(".hint-signup-message", "none");
    View.clearInputs(
      "signup-name",
      "signup-account-id",
      "signup-email",
      "signup-password"
    );
  });

  document.querySelector(".close-signin").addEventListener("click", () => {
    View.setElementDisplay(".signin-mask", "none"),
      View.setElementDisplay(".hint-signin-message", "none");
    View.clearInputs("signin-account-id", "signin-password");
  });

  document.querySelector(".close-signup").addEventListener("click", () => {
    View.setElementDisplay(".signup-mask", "none"),
      View.setElementDisplay(".hint-signup-message", "none"),
      View.clearInputs(
        "signup-name",
        "signup-account-id",
        "signup-email",
        "signup-password"
      );
  });

  document
    .querySelector(".signin")
    .addEventListener("submit", async (event) => {
      event.preventDefault();
      console.log("Form submitted");

      const formData = new FormData(event.target);
      const data = Object.fromEntries(formData.entries());

      let result = await Model.fetchApi(userSignInUrl, "PUT", data);
      result = stringifyObjectValues(result);
      if (result.ok) {
        localStorage.setItem("userToken", result.data.token);
        View.updateMessage(".hint-signin-message", "登入成功", true);
        View.clearInputs("signin-account-id", "signin-password");

        View.displayUserInterface(true);
        window.location.reload();
      } else {
        View.updateMessage(".hint-signin-message", result.message, false);
        View.clearInputs("signin-account-id", "signin-password");
      }
    });

  document
    .querySelector(".signup")
    .addEventListener("submit", async (event) => {
      event.preventDefault();

      const formData = new FormData(event.target);
      const data = Object.fromEntries(formData.entries());

      // 驗證：只能包含字母、數字、下底線
      const accountIdRegex = /^[a-zA-Z0-9_-]+$/;
      if (!accountIdRegex.test(data.account_id)) {
        View.updateMessage(
          ".hint-signup-message",
          "帳號只能包含字母、數字、下底線",
          false
        );
        return;
      }

      const result = await Model.fetchApi(userRegisterUrl, "POST", data);
      if (result.ok) {
        View.updateMessage(
          ".hint-signup-message",
          "註冊成功，請登入會員",
          true
        );
        View.clearInputs(
          "signup-name",
          "signup-account-id",
          "signup-email",
          "signup-password"
        );
        View.setElementDisplay(".signup-mask", "none");
        View.setElementDisplay(".signin-mask", "flex");
      } else {
        View.updateMessage(".hint-signup-message", result.message, false);
        View.clearInputs(
          "signup-name",
          "signup-account-id",
          "signup-email",
          "signup-password"
        );
      }
    });
}

export async function checkUserState(callback) {
  const token = localStorage.getItem("userToken");

  if (!token) {
    View.displayUserInterface(false);
    if (typeof callback === "function") {
      callback(null);
    }
    return false;
  }

  try {
    const result = await Model.fetchUserState(token);
    // console.log("result.status:", result.status);
    if (result && result.message === "Failed to get user's data") {
      localStorage.clear();
      window.location.href = "/";
      console.log("Token 已過期");
      return false;
    }

    if (result) {
      // console.log("result:", result);
      View.displayUserInterface(true);
      localStorage.setItem("userName", result.name);
      localStorage.setItem("account_id", result.account_id);

      if (typeof callback === "function") {
        callback(result);
      }

      return true;
    } else {
      throw new Error("無法驗證用戶狀態");
    }
  } catch (error) {
    console.error("驗證用戶狀態失敗：", error);
    View.displayUserInterface(false);

    localStorage.clear();
    window.location.href = "/";
    return false;
  }
}

export function setupLogoutListener() {
  const logout = document.querySelector(".logout");
  logout.addEventListener("click", logOut);
}

function logOut() {
  Model.clearUserSession();

  window.location.reload();
  window.location.href = "/";
  localStorage.clear();
}

export function initialize() {
  setupEventListeners();
  setupLogoutListener();
}

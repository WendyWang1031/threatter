export function setElementDisplay(selector, display) {
  const element = document.querySelector(selector);
  element.style.display = display;
}

export function updateMessage(selector, message, isSuccess) {
  const element = document.querySelector(selector);
  element.textContent = message;
  element.style.color = isSuccess ? "#666666" : "red";
  element.style.display = "block";
}

export function clearInputs(...selectors) {
  selectors.forEach((selector) => {
    document.getElementById(selector).value = "";
  });
}

export function displayUserInterface(isLoggedIn) {
  const loginSignin = document.querySelector(".login-signin");
  const logout = document.querySelector(".logout");
  if (isLoggedIn) {
    loginSignin.style.display = "none";
    logout.style.display = "flex";
  } else {
    loginSignin.style.display = "flex";
    logout.style.display = "none";
  }
}

export function signUpSignInDisplayNone() {
  const signinMask = document.querySelector(".signin-mask");
  const signupMask = document.querySelector(".signup-mask");
  signinMask.style.display = "none";
  signupMask.style.display = "none";
}

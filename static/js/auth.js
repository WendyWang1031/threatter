import { initialize, checkUserState } from "./controller/controller_auth.js";
import { signUpSignInDisplayNone } from "./view/view.js";

document.addEventListener("DOMContentLoaded", function () {
  signUpSignInDisplayNone();
  initialize();
  checkUserState();
});

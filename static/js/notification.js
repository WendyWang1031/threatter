import { PermissionAllIcon } from "./view/view_icon.js";

import { setupTabSwitching } from "./controller/controller_notification.js";

document.addEventListener("DOMContentLoaded", async function () {
  PermissionAllIcon();

  setupTabSwitching();
});

export function updateMessage(selector, message) {
  const element = document.getElementById(selector);
  element.textContent = message;
  element.style.display = "block";
}

export function displayCreatePostAccount() {
  const account_id_value = localStorage.getItem("account_id");
  const account_id = document.querySelector(".account_id");
  account_id.textContent = account_id_value;
}

export function displayMemberDetail(data) {
  const accountIdSpan = document.querySelector(".create_content_account_id");

  accountIdSpan.textContent = data.account_id;
  if (data.avatar) {
    const avatarCreatePost = document.querySelector(
      ".profile-pic-create-content"
    );
    if (avatarCreatePost) {
      const imgCreatePost = document.createElement("img");
      imgCreatePost.src = data.avatar;
      imgCreatePost.classList.add("profile-pic");
      avatarCreatePost.replaceWith(imgCreatePost);
    }

    const avatarUserInfoPost = document.querySelector(".user-info-profile-pic");
    if (avatarUserInfoPost) {
      const imgUserInfoPost = document.createElement("img");
      imgUserInfoPost.src = data.avatar;
      imgUserInfoPost.classList.add("profile-pic");
      avatarUserInfoPost.replaceWith(imgUserInfoPost);
    }
  } else {
    const icon = document.createElement("i");
    icon.classList.add("fa-regular", "fa-circle-user", "profile-pic");
  }
}

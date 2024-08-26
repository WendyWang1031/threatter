import { uploadMediaFile } from "./controller_upload.js";

function buildUrl({ accountId, postId, commentId, type }) {
  const baseUrl = "/api/member";

  if (type === "post") {
    // 發布新貼文
    return "/api/post";
  } else if (type === "comment") {
    // 在貼文底下發表評論
    return `${baseUrl}/${encodeURIComponent(
      accountId
    )}/post/${encodeURIComponent(postId)}/reply`;
  } else if (type === "reply") {
    // 回覆評論
    if (commentId) {
      return `${baseUrl}/${encodeURIComponent(
        accountId
      )}/post/${encodeURIComponent(postId)}/comment/${encodeURIComponent(
        commentId
      )}/reply`;
    } else {
      throw new Error("Missing commentId for reply type");
    }
  } else {
    throw new Error("Invalid type provided");
  }
}

export function validateForm(type, accountId, postId, commentId) {
  const content = document.querySelector(".post-input").value;

  // 根據 type 設置 visibility
  let visibility = "public";
  if (type === "post") {
    const privacySelect = document.getElementById("privacy-options");
    visibility = privacySelect.value;
  }

  // 初始媒體類型的值
  let imageFile = null;
  let videoFile = null;
  let audioFile = null;

  // 抓取所有媒體類型
  const imageUploadInput = document.getElementById("image-upload");
  const videoUploadInput = document.getElementById("video-upload");
  const audioUploadInput = document.getElementById("audio-upload");

  if (imageUploadInput.files.length > 0) {
    imageFile = imageUploadInput.files[0];
  }
  if (videoUploadInput.files.length > 0) {
    videoFile = videoUploadInput.files[0];
  }
  if (audioUploadInput.files.length > 0) {
    audioFile = audioUploadInput.files[0];
  }
  console.log("videoUploadInput:", videoUploadInput);

  if (content === "" && !imageFile && !videoFile && !audioFile) {
    alert("請填寫文字欄位或上傳圖片、影片或音源");
    return false;
  }
  const url = buildUrl({ type, accountId, postId, commentId });
  submitData(content, imageFile, videoFile, audioFile, url, postId, visibility);
  return true;
}

async function submitData(
  content,
  imageFile,
  videoFile,
  audioFile,
  url,
  postId,
  visibility
) {
  document.getElementById("loading").classList.remove("hidden");

  let data = {
    content: {
      text: content,
      media: {
        images: null,
        videos: null,
        audios: null,
      },
    },
    visibility: visibility,
  };

  // 如果是新增貼文，設定 post_parent_id
  if (postId && url === "/api/post") {
    data.post_parent_id = postId | null;
  }

  // 圖片
  if (imageFile) {
    const imageUrl = await uploadMediaFile(imageFile);
    if (imageUrl) {
      data.content.media.images = imageUrl;
    }
  }

  // 影片
  if (videoFile) {
    const videoUrl = await uploadMediaFile(videoFile);
    if (videoUrl) {
      data.content.media.videos = videoUrl;
    }
  }

  // 音檔
  if (audioFile) {
    const audioUrl = await uploadMediaFile(audioFile);
    if (audioUrl) {
      data.content.media.audios = audioUrl;
    }
  }

  try {
    await fetchUpdateData(data, url);
  } catch (error) {
    console.error("Error submitting post:", error);
    alert("Failed to submit post: " + error.message);
  } finally {
    document.getElementById("loading").classList.add("hidden");
  }
}

async function fetchUpdateData(data, url) {
  document.getElementById("loading").classList.remove("hidden");
  const token = localStorage.getItem("userToken");

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    // console.log("body:", JSON.stringify(data));

    if (!response.ok) {
      console.log("Failed to post details:", response.status);

      throw new Error(`HTTP status ${response.status}`);
    } else {
      location.reload();
    }
  } catch (error) {
    console.error("Error updating data", error);
  } finally {
    document.getElementById("loading").classList.add("hidden");
  }
}

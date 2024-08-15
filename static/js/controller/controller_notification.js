export function setupIntersectionObserver() {
  const followerReqListContainer = document.querySelector(".notify-req-list");

  const observer = new IntersectionObserver(async (entries, observer) => {
    const [entry] = entries;
    if (entry.isIntersecting) {
      await fetchAndDisplayFollowReq(followerReqListContainer);

      observer.disconnect();
    }
  });

  observer.observe(followerReqListContainer);
}

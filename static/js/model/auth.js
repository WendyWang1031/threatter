const userSignInUrl = "/api/user/auth";
export async function fetchUserState(token) {
  try {
    const response = await fetch(userSignInUrl, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });
    const data = await response.json();
    // console.log("fetchUserState data:", data);
    return data;
  } catch (error) {
    console.error("Error Cheking User's State:", error);
    return { suceess: false, message: "Network error" };
  }
}

export async function fetchApi(url, method, data) {
  const headers = {
    "Content-Type": "application/json",
  };

  if (method == "GET" && localStorage.getItem("userToken")) {
    headers["Authorization"] = `Bearer ${localStorage.getItem("userToken")}`;
  }

  const options = {
    method: method,
    headers: headers,
    body: JSON.stringify(data),
  };

  if (method === "GET") {
    delete options.body;
  }

  try {
    const response = await fetch(url, options);
    if (response.ok) {
      const data = await response.json();
      return {
        ok: true,
        data: data,
      };
    } else {
      const errorData = await response.json();
      return {
        ok: false,
        message: errorData.message || "Something went wrong",
      };
    }

    return await response.json();
  } catch (error) {
    console.error("API Request Failed", error);
    return { ok: false, message: "Network error" };
  }
}

export function clearUserSession() {
  localStorage.removeItem("userToken");
  localStorage.removeItem("account_id");
  localStorage.removeItem("userName");
}

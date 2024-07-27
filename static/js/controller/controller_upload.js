export async function getPresignedUrl(file_name, file_type) {
  try {
    const response = await fetch("/api/post/generate-presigned-url_test", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ file_name, file_type }),
    });
    if (!response.ok) {
      throw new Error("Network response was not ok.");
    }
    return response.json();
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
}

export async function uploadFileToS3(presignedUrlData, file) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open("PUT", presignedUrlData, true);
    xhr.setRequestHeader("Content-Type", file.type);

    xhr.onload = () => {
      if (xhr.status === 200) {
        resolve();
      } else {
        reject(new Error("Failed to upload file."));
      }
    };

    xhr.onerror = () => {
      reject(new Error("Network error occurred."));
    };

    xhr.send(file);
  });
  //--------------BACKUP CODE--------------
  // console.log(
  //   "Presigned URL Data1:",
  //   JSON.stringify(presignedUrlData, null, 2)
  // );
  // console.log("Presigned URL 's post url:", presignedUrlData.url);
  // console.log(
  //   "Presigned URL fields Data fields :",
  //   JSON.stringify(presignedUrlData.fields, null, 2)
  // );
  // const formData = new FormData();
  // formData.append("key", presignedUrlData.fields.key);
  // formData.append("acl", presignedUrlData.fields.acl);
  // formData.append("Content-Type", presignedUrlData.fields["Content-Type"]);
  // formData.append("policy", presignedUrlData.fields.policy);
  // formData.append(
  //   "x-amz-algorithm",
  //   presignedUrlData.fields["x-amz-algorithm"]
  // );
  // formData.append(
  //   "x-amz-credential",
  //   presignedUrlData.fields["x-amz-credential"]
  // );
  // formData.append("x-amz-date", presignedUrlData.fields["x-amz-date"]);
  // formData.append(
  //   "x-amz-signature",
  //   presignedUrlData.fields["x-amz-signature"]
  // );
  // formData.append("file", file);
  // try {
  //   const uploadResponse = await fetch(presignedUrlData.url, {
  //     method: "POST",
  //     body: formData,
  //   });
  //   if (!uploadResponse.ok) {
  //     console.log("Upload failed with status:", uploadResponse.status);
  //     const text = await uploadResponse.text();
  //     console.log("Failed response text:", text);
  //     throw new Error("Failed to upload: " + uploadResponse.statusText);
  //   }
  //   const responseData = await uploadResponse.json();
  //   console.log("Upload successful:", responseData);
  //   return responseData;
  // } catch (error) {
  //   console.error("Error during fetch operation:", error);
  // }
  // // 列印 FormData 的內容
  // for (const pair of formData.entries()) {
  //   console.log(`${pair[0]}: ${pair[1]}`);
  // }
  // if (formData.has("file")) {
  //   console.log("File details:");
  //   const fileData = formData.get("file");
  //   console.log(`Name: ${fileData.name}`);
  //   console.log(`Type: ${fileData.type}`);
  //   console.log(`Size: ${fileData.size} bytes`);
  // }
  // try {
  //   const response = await fetch(presignedUrlData.url, {
  //     method: "POST",
  //     body: formData,
  //   });
  //   if (!response.ok) {
  //     const errorText = await response.text();
  //     console.error("Failed to upload file to S3. Response:", errorText);
  //     throw new Error("Failed to upload file to S3: " + errorText);
  //   }
  //   console.log("File uploaded successfully.");
  // } catch (error) {
  //   console.error("Error uploading file:", error);
  //   console.error("Response was:", error.response);
  //   throw error;
  // }

  // const xhr = new XMLHttpRequest();
  // xhr.open("PUT", presignedUrlData, true);
  // xhr.setRequestHeader("Content-Type", file.type);
  // xhr.upload.onprogress = function (e) {
  //   if (e.lengthComputable) {
  //     const percentComplete = (e.loaded / e.total) * 100;
  //     console.log(percentComplete + "% uploaded");
  //   }
  // };
  // xhr.send(file);
  // xhr.onload = function () {
  //   if (xhr.status == 200) {
  //     alert("File uploaded successfully");
  //   } else {
  //     alert("File upload failed");
  //   }
  // };
  // xhr.onerror = function () {
  //   alert("File upload failed");
  // };
}

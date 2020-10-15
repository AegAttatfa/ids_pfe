import http from "./http-common";

const upload = (file, onUploadProgress) => {
  let formData = new FormData();

  formData.append("file", file);
  const config = {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
  };
  return http
    .post("/upload", formData, {
      headers: {
        "Access-Control-Allow-Origin": "*",
      },
      onUploadProgress,
    })
    .then((res) => {
      return res.data;
    });
};

export default {
  upload,
};

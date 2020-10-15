import axios from "axios";

const getList = async () => {
  const config = {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
  };
  const res = await axios.get("/intrusions", config, {
    headers: {
      "Content-type": "application/json",
    },
  });
  return res.data;
};

export default getList;

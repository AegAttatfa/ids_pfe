import { Link } from "react-router-dom";
import React from "react";
const logout = ({ props }) => {
  return (
    <Link
      to="/"
      onClick={() => {
        localStorage.clear();
        this.props.history.push("/admin");
      }}
    />
  );
};

export default logout;

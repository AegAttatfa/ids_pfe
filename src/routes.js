import Dashboard from "views/Dashboard.js";
import AttcksList from "views/Attacks.js";
import UserPage from "views/User.js";
import Upload from "views/Upload";
import logout from "views/Logout";
var routes = [
  {
    path: "/dashboard",
    name: "Dashboard",
    icon: "nc-icon nc-bank",
    component: Dashboard,
    layout: "/admin",
  },

  {
    path: "/user",
    name: "User Profile",
    icon: "nc-icon nc-single-02",
    component: UserPage,
    layout: "/admin",
  },
  {
    path: "/upload",
    name: "Upload",
    icon: "nc-icon nc-bell-55",
    component: Upload,
    layout: "/admin",
  },
  {
    path: "/attacks",
    name: "Journal",
    icon: "nc-icon nc-tile-56",
    component: AttcksList,
    layout: "/admin",
  },
  {
    path: "/login",
    name: "Logout",
    icon: "nc-icon nc-stre-right",
    component: logout,
    layout: "/admin",
  },
];
export default routes;

// src/index.js
// This is the entry point of our React app.
// ChatGPT says this means "This is the first JavaScript file that actually starts your app running in the browser."
// It takes the <App /> component and renders it into the HTML page (public/index.html).

import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";

const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

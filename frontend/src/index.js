// src/index.js
// This is the entry point of our React app.
// ChatGPT says this means "This is the first JavaScript file that actually starts your app running in the browser."
// It takes the <App /> component and renders it into the HTML page (public/index.html).

import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css"; // Global styles applied to the whole page
import App from "./App"; // Our main application component

// Create a React "root" and attach it to the <div id="root"></div>
// in public/index.html. This is where our whole React app will live.
const root = ReactDOM.createRoot(document.getElementById("root"));

// Render the <App /> component inside the root.
// <React.StrictMode> adds extra checks in development
// It's optional, but recommended. You can remove it if it confuses you.
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

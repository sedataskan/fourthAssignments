import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import { PrimeReactProvider } from "primereact/api";
import "primereact/resources/primereact.css";
import "primereact/resources/themes/saga-orange/theme.css";
import "primeflex/primeflex.css";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <PrimeReactProvider>
      <App />
    </PrimeReactProvider>
  </React.StrictMode>
);

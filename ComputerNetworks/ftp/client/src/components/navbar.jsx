import React from "react";
import { LinearGradient } from "react-text-gradients";
import { Toast } from "primereact/toast";
import { useRef } from "react";
import Upload from "./upload";
import Download from "./download";

const Navbar = () => {
  const toastBottomRight = useRef(null);

  const showMessage = (event, ref, severity) => {
    const label = event.target.innerText;
    const message = event.target.getAttribute("content");

    ref.current.show({
      severity: severity,
      summary: label,
      detail: message,
      life: 3000,
    });
  };
  return (
    <nav className="navbar">
      <h1>
        <LinearGradient
          gradient={["to left", "rgb(255, 136, 0), rgb(255, 0, 0)"]}
        >
          FTP App
        </LinearGradient>
      </h1>

      <div className="buttons">
        <Toast ref={toastBottomRight} position="bottom-right" />
        <button
          className="path-create button"
          onClick={(e) => showMessage(e, toastBottomRight, "success")}
          content="Path created successfully!"
        >
          <i className="fas fa-plus"></i> path-create
        </button>
        <button
          className="path-delete button"
          onClick={(e) => showMessage(e, toastBottomRight, "warn")}
          content="Path deleted successfully!"
        >
          <i className="fas fa-trash"></i> path-delete
        </button>
        <button
          className="file-edit button"
          onClick={(e) => showMessage(e, toastBottomRight, "info")}
          content="File edited successfully!"
        >
          <i className="fas fa-edit"></i> file-edit
        </button>
        <button
          className="file-delete button"
          onClick={(e) => showMessage(e, toastBottomRight, "warn")}
          content="File deleted successfully!"
        >
          <i className="fas fa-trash"></i> file-delete
        </button>
        <button
          className="path-change button"
          onClick={(e) => showMessage(e, toastBottomRight, "info")}
          content="Path changed successfully!"
        >
          <i className="fas fa-exchange-alt"></i> path-change
        </button>

        <Upload />

        <Download />
      </div>
    </nav>
  );
};

export default Navbar;

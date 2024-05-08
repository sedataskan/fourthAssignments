import React from "react";
import { Toast } from "primereact/toast";
import { useRef, useState } from "react";
import { ProgressBar } from "primereact/progressbar";
import { Button } from "primereact/button";

const Download = () => {
  const toast = useRef(null);
  const [progress, setProgress] = useState(0);
  const interval = useRef(null);

  const clear = () => {
    setProgress(0);
    toast.current.clear();
    clearInterval(interval.current);
    interval.current = undefined;
  };

  const show = () => {
    if (!interval.current) {
      toast.current.show({
        summary: "Downloading files.",
      });

      setProgress(0);

      if (interval.current) {
        clearInterval(interval.current);
      }

      interval.current = setInterval(() => {
        setProgress((prevProgress) => {
          const newProgress = prevProgress + 20;

          if (newProgress >= 100) {
            clearInterval(interval.current);

            return 100;
          }

          return newProgress;
        });
      }, 1000);
    }
  };

  return (
    <>
      <Toast
        ref={toast}
        content={({ message }) => (
          <section
            className="flex p-3 gap-3 w-full bg-black-alpha-90 shadow-2 fadeindown"
            style={{ borderRadius: "10px" }}
          >
            <i className="pi pi-cloud-upload text-primary-500 text-2xl"></i>
            <div className="flex flex-column gap-3 w-full">
              <p className="m-0 font-semibold text-base text-white">
                {message.summary}
              </p>
              <p className="m-0 text-base text-700">{message.detail}</p>
              <div className="flex flex-column gap-2">
                <ProgressBar value={progress} showValue="false"></ProgressBar>
                <label className="text-right text-xs text-white">
                  {progress}% downloaded...
                </label>
              </div>
              <div className="flex gap-3 mb-3">
                {progress === 100 && (
                  <Button
                    label="Close"
                    icon="fas fa-check"
                    onClick={clear}
                    style={{ color: "#000" }}
                  />
                )}
                {progress !== 100 && (
                  <Button label="Cancel" icon="fas fa-xmark" onClick={clear} />
                )}
              </div>
            </div>
          </section>
        )}
      ></Toast>

      <button className="file-download button" onClick={show}>
        <i className="fas fa-download"></i> file-download
      </button>
    </>
  );
};

export default Download;

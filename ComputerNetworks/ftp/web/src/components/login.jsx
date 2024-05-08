import React, { useState } from "react";
import { Button } from "primereact/button";
import { Dialog } from "primereact/dialog";
import { InputText } from "primereact/inputtext";

export default function Login() {
  const [visible, setVisible] = useState(true);

  return (
    <div className="card flex justify-content-center">
      <Dialog
        visible={visible}
        modal
        onHide={() => setVisible(false)}
        content={({ hide }) => (
          <div
            className="flex flex-column px-8 py-5 gap-4"
            style={{
              borderRadius: "12px",
              backgroundImage:
                "radial-gradient(circle at left top, var(--primary-400), var(--primary-700))",
            }}
          >
            <label>
              <h2 className="text-primary-50 font-semibold">
                <i className="fas fa-users"></i> {""}Connection
              </h2>
            </label>
            <div className="inline-flex flex-column gap-2">
              <label htmlFor="domain" className="text-primary-50 font-semibold">
                Address
              </label>
              <InputText
                id="address"
                label="Address"
                className="bg-white-alpha-20 border-none p-3 text-primary-50"
                type="text"
              ></InputText>
            </div>
            <div className="inline-flex flex-column gap-2">
              <label
                htmlFor="username"
                className="text-primary-50 font-semibold"
              >
                Username
              </label>
              <InputText
                id="username"
                label="Username"
                className="bg-white-alpha-20 border-none p-3 text-primary-50"
              ></InputText>
            </div>
            <div className="inline-flex flex-column gap-2">
              <label
                htmlFor="password"
                className="text-primary-50 font-semibold"
              >
                Password
              </label>
              <InputText
                id="password"
                label="Password"
                className="bg-white-alpha-20 border-none p-3 text-primary-50"
                type="password"
              ></InputText>
            </div>

            <div className="flex align-items-center gap-2">
              <Button
                label="Sign In"
                onClick={(e) => hide(e)}
                text
                className="p-3 w-full text-primary-50 border-1 border-white-alpha-30 hover:bg-white-alpha-10"
              ></Button>
            </div>
          </div>
        )}
      ></Dialog>
    </div>
  );
}

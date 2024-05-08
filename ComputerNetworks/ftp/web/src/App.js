import "./App.css";
import Navbar from "./components/navbar";
import Console from "./components/console";
import { useState } from "react";

function App() {
  const [value, setValue] = useState(false);
  return (
    <div className="App">
      <header className="App-header">
        <Navbar />
        <Console
          isOn={value}
          handleToggle={() => setValue(!value)}
          onColor="#f3aa21"
        />
        {/* <footer>
          <i>
            Made with{" "}
            <i
              className="fas fa-heart"
              style={{
                color: "red",
              }}
            ></i>{" "}
            by Seda Nur Taşkan | 201180004 for BM402
          </i>
        </footer> */}
      </header>
    </div>
  );
}

export default App;

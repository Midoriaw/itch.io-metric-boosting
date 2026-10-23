import React, { useEffect, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";
import artwork from "./assets/destroy-planet-reference.png";

const SPEEDS = {
  slow: "SLOW",
  medium: "NORMAL",
  fast: "FAST"
};

function Corners() {
  return (
    <>
      <i className="corner tl">+</i>
      <i className="corner tr">+</i>
      <i className="corner bl">+</i>
      <i className="corner br">+</i>
    </>
  );
}

function Sidebar({ running, onStop }) {
  return (
    <aside className="sidebar">
      <div className="brand">
        <span className="brand-mark" />
        <span>D:ROCHILA</span>
      </div>

      <div className="side-divider" />

      <div className="side-label">
        <span>MODULE</span>
        <span>01</span>
      </div>

      <button className="side-item active">
        <span className="glyph">◈</span>
        ITCH.IO
        <small>01</small>
      </button>

      <button className="side-item">
        <span className="glyph">♫</span>
        TIKTOK
        <small>02</small>
      </button>

      <div className="side-divider thin" />

      <div className="side-label">
        <span>SYSTEM</span>
        <span>//</span>
      </div>

      <div className={`side-state ${running ? "online" : ""}`}>
        <span className="state-dot" />
        <span>{running ? "EXECUTION" : "STANDBY"}</span>
      </div>

      {running && (
        <button className="side-item danger" onClick={onStop}>
          <span className="glyph">×</span>
          TERMINATE
          <small>!!</small>
        </button>
      )}

      <div className="side-bottom">
        <div className="jp-box">
          <Corners />
          <div className="jp">夢 終 夜</div>
          <div className="jp-line">DESTROY / PLANET</div>
          <div className="jp-line">NO SIGNAL // 0x01</div>
        </div>

        <div className="side-meta">
          <span>SYS://DROCHILA</span>
          <span>BUILD 2.0</span>
        </div>
      </div>
    </aside>
  );
}

function Field({ label, children }) {
  return (
    <div className="field">
      <label>{label}</label>
      {children}
    </div>
  );
}

function SetupPanel({
  url,
  setUrl,
  cycles,
  setCycles,
  speed,
  setSpeed,
  running,
  onStart
}) {
  return (
    <section className="setup-panel">
      <Corners />

      <div className="panel-tag">PROTOCOL / CONFIGURATION</div>

      <div className="target-title">
        <span className="target-index">01</span>
        <div>
          <div className="target-kicker">TARGET DEFINITION</div>
          <h3>ITCH.IO / GAME URL</h3>
        </div>
      </div>

      <Field label="TARGET URL">
        <div className="url-input">
          <span>&gt;</span>
          <input
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            disabled={running}
            spellCheck="false"
            placeholder="https://itch.io/game"
          />
        </div>
      </Field>

      <div className="two-fields">
        <Field label="EXECUTION COUNT">
          <input
            className="square-input"
            type="number"
            min="0"
            value={cycles}
            onChange={(e) => setCycles(e.target.value)}
            disabled={running}
          />
        </Field>

        <Field label="EXECUTION SPEED">
          <div className="select-input">
            <select
              value={speed}
              onChange={(e) => setSpeed(e.target.value)}
              disabled={running}
            >
              <option value="slow">SLOW</option>
              <option value="medium">NORMAL</option>
              <option value="fast">FAST</option>
            </select>
            <span>⌄</span>
          </div>
        </Field>
      </div>

      <div className="setup-divider" />

      <div className="ready-row">
        <span>&gt; STATUS:</span>
        <strong>{running ? "EXECUTION_ACTIVE" : "READY_TO_RUN"}</strong>
      </div>

      <button className="protocol-button" onClick={onStart} disabled={running}>
        <span>▶</span>
        {running ? "PROTOCOL_ACTIVE" : "START_PROTOCOL"}
      </button>

      <div className="microcopy">
        <span>ENTER → TARGET</span>
        <span>0 → INFINITE</span>
      </div>
    </section>
  );
}

function Terminal({ logs }) {
  return (
    <section className="terminal">
      <Corners />

      <div className="terminal-top">
        <span><i className="terminal-dot" /> BACKEND_STREAM</span>
        <span className="red-text">LIVE</span>
      </div>

      <div className="terminal-content">
        {logs.length === 0 ? (
          <>
            <div className="log dim">[00:00:00] awaiting protocol...</div>
            <div className="log">[SYSTEM] python bridge initialized</div>
            <div className="log dim">[SYSTEM] no active process</div>
          </>
        ) : logs.map((line, index) => (
          <div className="log" key={`${line}-${index}`}>{line}</div>
        ))}
      </div>

      <div className="terminal-bottom">
        <span>STREAM://PYTHON</span>
        <span>ENC:LOCAL</span>
      </div>
    </section>
  );
}

function BrowserPanel({ url, browserRef }) {
  const [address, setAddress] = useState(url);

  useEffect(() => setAddress(url), [url]);

  const goBack = () => browserRef.current?.goBack();
  const goForward = () => browserRef.current?.goForward();
  const reload = () => browserRef.current?.reload();

  return (
    <section className="browser-shell">
      <Corners />

      <div className="browser-toolbar">
        <div className="browser-actions">
          <button onClick={goBack}>‹</button>
          <button onClick={goForward}>›</button>
          <button onClick={reload}>↻</button>
        </div>

        <div className="browser-address">
          <span className="address-lock">◆</span>
          <span>{address}</span>
        </div>

        <span className="browser-live">WEBVIEW / LIVE</span>
      </div>

      <webview
        ref={browserRef}
        className="webview"
        src={url}
        allowpopups="true"
        partition="persist:drochila"
        webpreferences="contextIsolation=yes"
      />
    </section>
  );
}

function RunningHUD({ cycles, launchCount, onStop }) {
  return (
    <aside className="running-hud">
      <div className="hud-title">
        <span>EXECUTION_MONITOR</span>
        <span>02/03</span>
      </div>

      <div className="hud-metric">
        <span>LAUNCH_COUNT</span>
        <strong>{String(launchCount).padStart(2, "0")}</strong>
      </div>

      <div className="hud-metric compact">
        <span>REQUESTED</span>
        <strong>{cycles === "0" ? "∞" : String(cycles).padStart(2, "0")}</strong>
      </div>

      <div className="hud-status">
        <span>&gt; STATUS:</span>
        <strong>READY_TO_RUN</strong>
      </div>

      <div className="hud-progress">
        <span />
      </div>

      <button className="terminate-button" onClick={onStop}>
        <span>■</span>
        TERMINATE
      </button>
    </aside>
  );
}

function App() {
  const [phase, setPhase] = useState(1);
  const [url, setUrl] = useState("https://itch.io");
  const [cycles, setCycles] = useState("0");
  const [speed, setSpeed] = useState("medium");
  const [logs, setLogs] = useState([]);
  const [launchCount, setLaunchCount] = useState(0);

  const browserRef = useRef(null);

  const log = (message) => {
    const now = new Date().toLocaleTimeString("en-GB");
    setLogs((prev) => [...prev.slice(-120), `[${now}] ${message}`]);
  };

  useEffect(() => {
    if (!window.electronAPI?.onBotLog) return;
    return window.electronAPI.onBotLog((message) => log(message));
  }, []);

  const start = async () => {
    if (!url.trim()) {
      log("[ERROR] target URL is empty");
      return;
    }

    const payload = {
      url: url.trim(),
      cycles: Number(cycles) || 0,
      speed: SPEEDS[speed]
    };

    setPhase(2);
    setLaunchCount(0);

    log("[UI] START_PROTOCOL");
    log(`[UI] TARGET ${payload.url}`);
    log(`[UI] CYCLES ${payload.cycles}`);
    log(`[UI] SPEED ${payload.speed}`);

    await window.electronAPI?.startBot?.(payload);
  };

  const stop = async () => {
    await window.electronAPI?.stopBot?.();
    setPhase(1);
    log("[UI] TERMINATE");
  };

  return (
    <main className={`app phase-${phase}`}>
      <div className="grain" />

      <Sidebar running={phase === 2} onStop={stop} />

      <section className="workspace">
        <header className="topbar">
          <div>
            <span className="phase-code">
              {phase === 1 ? "FAZA_1 // CONFIGURATION" : "FAZA_2 // EXECUTION"}
            </span>
            <h1>{phase === 1 ? "DESTROY PROTOCOL" : "LIVE AUTOMATION"}</h1>
          </div>

          <div className="top-status">
            <span className="top-dot" />
            {phase === 1 ? "STANDBY" : "ONLINE"}
          </div>
        </header>

        {phase === 1 ? (
          <section className="phase-one">
            <div className="art">
              <img src={artwork} alt="" />
              <div className="art-fade" />
              <div className="art-scan" />
            </div>

            <div className="poster-title">
              <div className="poster-small">SYSTEM / 0x01</div>
              <h2>DESTROY</h2>
              <h2>THE PLANET</h2>
              <div className="poster-orbit">✦ ◎ ✦</div>
              <p>NO SIGNAL / NO ORDINARY</p>
            </div>

            <div className="poster-stars">★ ★ ✦</div>

            <div className="setup-wrap">
              <SetupPanel
                url={url}
                setUrl={setUrl}
                cycles={cycles}
                setCycles={setCycles}
                speed={speed}
                setSpeed={setSpeed}
                running={false}
                onStart={start}
              />
            </div>
          </section>
        ) : (
          <section className="phase-two">
            <div className="execution-grid">
              <BrowserPanel url={url} browserRef={browserRef} />

              <div className="execution-bottom">
                <Terminal logs={logs} />
                <RunningHUD
                  cycles={cycles}
                  launchCount={launchCount}
                  onStop={stop}
                />
              </div>
            </div>
          </section>
        )}
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);
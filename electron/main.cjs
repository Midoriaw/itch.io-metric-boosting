const { app, BrowserWindow, ipcMain } = require("electron");
const path = require("path");
const { spawn } = require("child_process");

let mainWindow;
let pythonProcess;

const dev = !app.isPackaged;

function sendLog(message) {
  if (mainWindow && !mainWindow.isDestroyed()) {
    mainWindow.webContents.send("bot:log", message);
  }
}

function stopPython() {
  if (pythonProcess && !pythonProcess.killed) {
    pythonProcess.kill();
  }
  pythonProcess = undefined;
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 820,
    minWidth: 1100,
    minHeight: 700,
    backgroundColor: "#080808",
    autoHideMenuBar: true,
    webPreferences: {
      preload: path.join(__dirname, "preload.cjs"),
      contextIsolation: true,
      nodeIntegration: false,
      webviewTag: true,
      sandbox: false
    }
  });

  if (dev) {
    mainWindow.loadURL("http://127.0.0.1:5173");
  } else {
    mainWindow.loadFile(path.join(__dirname, "..", "dist", "index.html"));
  }

  mainWindow.on("closed", () => {
    stopPython();
    mainWindow = undefined;
  });
}

ipcMain.handle("bot:start", (_event, payload) => {
  stopPython();

  const script = path.join(__dirname, "..", "backend", "bot_stub.py");
  // Запускаем без передачи аргументов в массив, так как скрипт слушает stdin
  pythonProcess = spawn("python", [script], {
    windowsHide: true
  });

  pythonProcess.stdout.on("data", (data) => {
    data.toString().split(/\r?\n/).filter(Boolean).forEach((line) => {
      try {
        // Пытаемся распарсить лог из Python-формата
        const parsed = JSON.parse(line);
        if (parsed && parsed.type === "log") {
          sendLog(parsed.message); // Отправляем чистый текст сообщения во фронтенд
        } else {
          sendLog(line);
        }
      } catch (e) {
        // Если это не JSON, отправляем строку "как есть"
        sendLog(line);
      }
    });
  });

  pythonProcess.stderr.on("data", (data) => {
    data.toString().split(/\r?\n/).filter(Boolean)
      .forEach((line) => sendLog(`[PYTHON_ERROR] ${line}`));
  });

  pythonProcess.on("close", (code) => {
    sendLog(`[PYTHON] process exited with code ${code ?? 0}`);
    pythonProcess = undefined;
  });

  // Передаем команду СТАРТ и payload в поток stdin Python-процесса
  const startCommand = JSON.stringify({ cmd: "start", ...payload });
  pythonProcess.stdin.write(startCommand + "\n");

  sendLog("[ELECTRON] PYTHON_BRIDGE ONLINE");
  return { ok: true };
});

ipcMain.handle("bot:stop", () => {
  if (pythonProcess) {
    try {
      // Корректно отправляем команду стоп в stdin перед жестким завершением
      pythonProcess.stdin.write(JSON.stringify({ cmd: "stop" }) + "\n");
    } catch (e) {}
  }
  stopPython();
  sendLog("[ELECTRON] PYTHON_BRIDGE TERMINATED");
  return { ok: true };
});

app.whenReady().then(() => {
  createWindow();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});

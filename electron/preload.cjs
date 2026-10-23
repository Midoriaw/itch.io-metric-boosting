const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("electronAPI", {
  startBot: (payload) => ipcRenderer.invoke("bot:start", payload),
  stopBot: () => ipcRenderer.invoke("bot:stop"),
  onBotLog: (callback) => {
    const listener = (_event, message) => callback(message);
    ipcRenderer.on("bot:log", listener);
    return () => ipcRenderer.removeListener("bot:log", listener);
  }
});
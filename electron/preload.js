/**
 * Electron 预加载脚本
 * 在渲染进程中暴露安全的 API
 */

const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  getBackendUrl: () => ipcRenderer.invoke('get-backend-url')
});


/**
 * Electron 主进程
 * 管理窗口创建和 Python 后端进程
 */

const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let pythonProcess;

// Python 后端进程管理
function startPythonBackend() {
  console.log('🚀 启动 Python 后端服务...');
  
  // 启动 Python 后端
  pythonProcess = spawn('python', ['backend_api.py'], {
    cwd: path.join(__dirname, '..'),
    stdio: 'pipe'
  });

  pythonProcess.stdout.on('data', (data) => {
    console.log(`[Python] ${data.toString()}`);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`[Python Error] ${data.toString()}`);
  });

  pythonProcess.on('close', (code) => {
    console.log(`Python 后端进程退出，代码: ${code}`);
  });

  // 等待后端启动
  return new Promise((resolve) => {
    setTimeout(() => {
      console.log('✅ Python 后端服务已启动');
      resolve();
    }, 3000);
  });
}

function stopPythonBackend() {
  if (pythonProcess) {
    console.log('🛑 关闭 Python 后端服务...');
    pythonProcess.kill();
    pythonProcess = null;
  }
}

// 创建主窗口
async function createWindow() {
  // 先启动 Python 后端
  await startPythonBackend();

  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    title: 'AI 智能切题工具',
    icon: path.join(__dirname, '../assets/icon.png') // 可选
  });

  // 开发环境加载 Vite 开发服务器
  if (process.env.NODE_ENV === 'development') {
    mainWindow.loadURL('http://localhost:5173');
    mainWindow.webContents.openDevTools();
  } else {
    // 生产环境加载打包后的文件
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'));
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// 应用准备就绪
app.whenReady().then(createWindow);

// 所有窗口关闭时退出应用（macOS 除外）
app.on('window-all-closed', () => {
  stopPythonBackend();
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// macOS 激活应用时重新创建窗口
app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// 应用退出前清理
app.on('before-quit', () => {
  stopPythonBackend();
});

// IPC 通信示例（可选）
ipcMain.handle('get-backend-url', () => {
  return 'http://localhost:8000';
});


const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');

let mainWindow;

function createMainWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    backgroundColor: '#020617', // Dark theme slate-950 background
    title: "نظام التذاكر والطباعة الصامتة",
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  function tryLoadServer() {
    if (!mainWindow || mainWindow.isDestroyed()) return;
    mainWindow.loadURL('http://localhost:5000/').catch((err) => {
      console.log("Waiting for backend server on port 5000...", err.message);
      if (mainWindow && !mainWindow.isDestroyed()) {
        mainWindow.loadFile(path.join(__dirname, 'offline.html')).catch(() => {});
        // Auto retry connecting every 2 seconds
        setTimeout(tryLoadServer, 2000);
      }
    });
  }

  tryLoadServer();

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(() => {
  createMainWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createMainWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// IPC Handler for multi-page ticket printing
ipcMain.on('print-ticket', (event, ticketHtml) => {
  console.log("[Printer] Single multi-page print order received. Sending to printer...");

  let printWindow = new BrowserWindow({
    show: false,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true
    }
  });

  printWindow.loadURL(`data:text/html;charset=utf-8,${encodeURIComponent(ticketHtml)}`);

  printWindow.webContents.on('did-finish-load', () => {
    console.log("[Printer] Multi-page print template loaded, sending to default printer driver...");
    
    printWindow.webContents.print({
      silent: true,
      printBackground: true,
      margins: { marginType: 'none' }
    }, (success, failureReason) => {
      if (!success) {
        console.error("[Printer] Print job failed:", failureReason);
      } else {
        console.log("[Printer] Multi-page print job completed successfully!");
      }
      
      try {
        if (printWindow && !printWindow.isDestroyed()) {
          printWindow.destroy();
        }
      } catch (err) {
        console.error("[Printer] Error destroying print window:", err);
      }
      printWindow = null;
    });
  });

  printWindow.webContents.on('did-fail-load', (e, errorCode, errorDescription) => {
    console.error("[Printer] Failed to load multi-page ticket HTML:", errorDescription);
    try {
      if (printWindow && !printWindow.isDestroyed()) {
        printWindow.destroy();
      }
    } catch (err) {}
    printWindow = null;
  });
});

const { contextBridge, ipcRenderer } = require('electron');

// Expose safe APIs to the renderer process
contextBridge.exposeInMainWorld('electron', {
  printTicket: (ticketHtml) => {
    ipcRenderer.send('print-ticket', ticketHtml);
  },
  printTickets: (ticketsHtmlArray) => {
    ipcRenderer.send('print-tickets', ticketsHtmlArray);
  }
});

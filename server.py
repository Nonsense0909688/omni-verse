const WebSocket = require('ws');
const fs = require('fs');

const PORT = process.env.PORT || 10000;
const wss = new WebSocket.Server({ port: PORT });

const LOG_FILE = 'chat_log.txt';
const clients = new Set();

function logMessage(msg) {
  const timestamp = new Date().toISOString();
  fs.appendFileSync(LOG_FILE, `[${timestamp}] ${msg}\n`);
}

wss.on('connection', (ws) => {
  clients.add(ws);
  ws.send("📢 Connected to Omni-Verse Chat!");

  ws.on('message', (message) => {
    const msg = message.toString();
    logMessage(msg);
    for (const client of clients) {
      if (client !== ws && client.readyState === WebSocket.OPEN) {
        client.send(msg);
      }
    }
  });

  ws.on('close', () => {
    clients.delete(ws);
  });
});

console.log(`✅ WebSocket server running on port ${PORT}`);

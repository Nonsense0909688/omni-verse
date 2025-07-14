const WebSocket = require('ws');
const fs = require('fs');
const PORT = process.env.PORT || 10000;

const server = new WebSocket.Server({ port: PORT });
const logFile = 'chat_log.txt';
const clients = new Set();

function log(msg) {
    const line = `[${new Date().toISOString()}] ${msg}\n`;
    fs.appendFileSync(logFile, line);
}

server.on('connection', ws => {
    clients.add(ws);
    ws.send('📢 Connected to Render Chat Server!');

    ws.on('message', message => {
        const msg = message.toString();
        log(msg);
        for (let client of clients) {
            if (client !== ws && client.readyState === WebSocket.OPEN) {
                client.send(msg);
            }
        }
    });

    ws.on('close', () => clients.delete(ws));
});

console.log(`✅ WebSocket server running on port ${PORT}`);

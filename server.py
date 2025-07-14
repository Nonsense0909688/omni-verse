import asyncio
import websockets
from datetime import datetime

PORT = 10000
clients = set()
LOG_FILE = "chat_log.txt"

async def log_message(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {message}\n")

async def handler(websocket, path):
    clients.add(websocket)
    await websocket.send("📢 Welcome to Python Render Chat!")

    try:
        async for message in websocket:
            msg = f"{message}"
            await log_message(msg)

            # Broadcast to all other clients
            await asyncio.gather(
                *[client.send(msg) for client in clients if client != websocket]
            )
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        clients.remove(websocket)

start_server = websockets.serve(handler, "0.0.0.0", PORT)

print(f"✅ Server running on port {PORT}")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

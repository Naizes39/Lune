import asyncio
import websockets

async def test_connection():
    uri = "ws://127.0.0.1:8000/ws/voice"
    async with websockets.connect(uri) as websocket:
        print("Connected to Lune.")
        await websocket.send("Testing the neural highway.")
        response = await websocket.recv()
        print(f"Received from server: {response}")

if __name__ == "__main__":
    asyncio.run(test_connection())
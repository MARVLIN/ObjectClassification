import websockets
import asyncio
import socket

PORT = 8080
HOST = socket.gethostbyname(socket.gethostname())

print(f'[Server is listening on] {HOST}:{PORT}')

connected = set()

async def echo(websocket, path):
    print('Client connected')
    connected.add(websocket)
    try:
        async for message in websocket:
            print(f'Message received: {message}')
            for conn in connected:
                if conn != websocket:
                    await conn.send(f'Message: {message}')
    except websockets.ConnectionClosed as e:
        print('Client left')
    finally:
        connected.remove(websocket)



start_server = websockets.serve(echo, HOST, PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

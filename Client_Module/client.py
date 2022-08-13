import websockets
import asyncio



async def listen():
    url = 'ws://23.254.176.188:8080'

    async with websockets.connect(url) as ws:
        await ws.send('Hello server')

        while True:
            msg = await ws.recv()
            print(msg)


asyncio.get_event_loop().run_until_complete(listen())

import asyncio
import websockets
import json


async def hello():
    websocket = await websockets.connect('ws://localhost:8765/build')

    while True:
        greeting = json.loads(await websocket.recv())
        print("< {}".format(greeting))
        greeting['resp'] = 'Build completed!'
        resp = json.dumps(greeting)
        await websocket.send(resp)
        print("> {}".format(resp))


asyncio.get_event_loop().run_until_complete(hello())

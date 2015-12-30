import asyncio
import websockets
import json


async def ping(websocket):
    while True:
        await websocket.ping()
        print('ping')
        await asyncio.sleep(30)


async def hello():
    websocket = await websockets.connect('ws://slackbooot.herokuapp.com/build')
    asyncio.ensure_future(ping(websocket))

    while True:
        greeting = json.loads(await websocket.recv())
        print("< {}".format(greeting))
        greeting['resp'] = 'Build completed!'
        resp = json.dumps(greeting)
        await websocket.send(resp)
        print("> {}".format(resp))


loop = asyncio.get_event_loop()
loop.run_until_complete(hello())

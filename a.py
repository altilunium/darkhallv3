import asyncio
import websockets

global_user = {}

async def handler(websocket):
	global global_user
	#print("Running at localhost:8001")
	board = await websocket.recv()
	if board not in global_user:
		global_user[board] = set()
	global_user[board].add(websocket)
	msg2 = "Current online user : " + str(len(global_user[board]))
	await websocket.send(msg2)
	websockets.broadcast(global_user[board],msg2)
	#print(board)
	#print(global_user)
	#await websocket.send("Connected")
	while True:
		try:
			msg = await websocket.recv()
			#print(msg)
			websockets.broadcast(global_user[board],msg)
		except:
			global_user[board].remove(websocket)
			msg2 = "Current online user : " + str(len(global_user[board]))
			websockets.broadcast(global_user[board],msg2)


	


async def main():
	async with websockets.serve(handler,"localhost",8001):
		await asyncio.Future() #run forever

if __name__ == "__main__":
	asyncio.run(main())
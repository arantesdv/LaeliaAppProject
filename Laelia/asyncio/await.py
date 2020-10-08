import asyncio


async def func():
	print("start")
	response = await asyncio.sleep(2)
	print("end", response)


asyncio.run(func)
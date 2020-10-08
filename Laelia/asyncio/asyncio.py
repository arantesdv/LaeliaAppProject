
# -*- coding: utf-8 -*-
import asyncio


async def func1():
    print(1)
    await asyncio.sleep(2)  # Automatically switch to other tasks in tasks in case of IO time-consuming operation
    print(2)


async def func2():
    print(3)
    await asyncio.sleep(2)  # Automatically switch to other tasks in tasks in case of IO time-consuming operation
    print(4)


tasks = [
    asyncio.wait(func1()),
    asyncio.wait(func2()),
]

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

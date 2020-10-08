# -*- coding: utf-8 -*-
import asyncio
import aiohttp


async def fetch(session, url):
    print("Send request")
    async with session.get(url, verify_ssl=False) as response:
        content = await response.content.read()
        file_name = url.rsplit("/")[-1]
        with open(file_name, mode="wb") as file_object:
            file_object.write(content)
        print("Download complete", url)


async def main():
    async with aiohttp.ClientSession() as session:
        url_list = [
            "http://ww1.sinaimg.cn/mw600/00745YaMgy1gedxxa59lyj30kk10p77m.jpg",
            "http://ww1.sinaimg.cn/mw600/00745YaMgy1gedxrlhlhaj30kk0dpmxj.jpg",
            "http://ww1.sinaimg.cn/mw600/00745YaMgy1gedxrlrw4tj30kk0pp78u.jpg"
        ]

        tasks = [asyncio.create_task(fetch(session, url)) for url in url_list]
        await asyncio.wait(tasks)

if __name__ == "__main__":
    asyncio.run(main())
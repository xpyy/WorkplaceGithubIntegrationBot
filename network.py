import os

from lxml import html
import aiohttp

FB_ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

FB_MESSAGE_URL = os.getenv('FB_URL')
FB_MESSAGE_PARAMS = {'access_token': FB_ACCESS_TOKEN}


async def get_title_from_url(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            content = await resp.text()
            parsed_content = html.fromstring(content)
            return parsed_content.find(".//title").text


async def send_message(user_id: int, message: str) -> None:
    data = {
        'recipient': {'id': user_id},
        'message': {'text': message},
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(FB_MESSAGE_URL, json=data, params=FB_MESSAGE_PARAMS) as resp:
            if resp.status >= 400:
                print('Something went wrong. Got %s response status. Content: %s', resp.status, await resp.read())

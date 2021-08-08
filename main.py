import os

from fastapi import Request, Response, FastAPI

from network import get_title_from_url, send_message

app = FastAPI()

EXPECTED_TOKEN = os.getenv('VERIFY_TOKEN')


@app.post('/messages/receive/')
async def receive_message(request: Request):
    print(await request.body())
    data = await request.json()
    for entry in data['entry']:
        for message in entry['messaging']:
            message_text = message['message']['text']
            try:
                response = await get_title_from_url(message_text)
            except:
                response = 'Something went wrong. Please sent correct URL'

            await send_message(message['sender']['id'], response)


@app.get('/messages/receive/')
async def receive_message_register(request: Request, response: Response):
    if (
        request.query_params.get('hub.verify_token') == EXPECTED_TOKEN
        and request.query_params.get('hub.mode') == 'subscribe'
    ):
        return Response(request.query_params.get('hub.challenge'))

    response.status_code = 403

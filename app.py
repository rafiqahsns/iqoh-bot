# mybot/app.py
import os
from decouple import config
from flask import (
    Flask, request, abort
)
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
app = Flask(__name__)
# get LINE_CHANNEL_ACCESS_TOKEN from your environment variable
line_bot_api = LineBotApi(
    config("LINE_CHANNEL_ACCESS_TOKEN",
           default=os.environ.get('LINE_ACCESS_TOKEN'))
)
# get LINE_CHANNEL_SECRET from your environment variable
handler = WebhookHandler(
    config("LINE_CHANNEL_SECRET",
           default=os.environ.get('LINE_CHANNEL_SECRET'))
)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):

    command = event.message.text.split(' ')[0]
    if command == "halo":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="hai qoh")
        )
    elif command == '/bday':
        name = event.message.text.split(' ')[1]
        birthday = event.message.text.split(' ')[2]
        wish = "happy birthday " + name + " " + birthday
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=wish)
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=first)
        )

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
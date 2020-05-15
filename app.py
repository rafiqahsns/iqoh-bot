# mybot/app.py
import os
from models import birthdays
from decouple import config
from flask import (
    Flask, request, abort
)
from flask_sqlalchemy import SQLAlchemy
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
app = Flask(__name__)

# set db
app.config['SQLALCHEMY_DATABASE_URI']           = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']    = False

db = SQLAlchemy(app)

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
def save_birthday(detail):
    birth_date = detail[0]
    name = " ".join(detail[1:])
    add_data = birthdays(
            name = name,
            birth_date = birth_date
        )
    try:
        db.session.add(add_data)
        db.session.commit()
        return('success')
    except:
        return('failed')

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):

    command = event.message.text.split(' ')[0]
    if command == "halo":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="hai qoh")
        )
    elif command == '/bday':
        detail = event.message.text.split(' ')[1:]
        response = save_birthday(detail)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response)
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.text.message)
        )

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
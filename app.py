# mybot/app.py
import os
from models import *
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
from sqlalchemy import extract
import datetime 

# app = Flask(__name__)
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
    db.session.add(add_data)
    db.session.commit()

def save_event(detail):
    date = detail[0]
    name = " ".join(detail[1:])
    add_data = events(
            name = name,
            date = date
        )
    db.session.add(add_data)
    db.session.commit()

def todaybday():
    result = birthdays.query.filter(extract('month', birthdays.birth_date) == datetime.date.today().month,
                                extract('day', birthdays.birth_date) == datetime.date.today().day).all()
    if result != []:
        birthday = "It's\n"
        for person in result:
            birthday = birthday + person.name +  "'s birthday\n"
    else:
        birthday = ""
    return(birthday)

def todayevent():
    result = events.query.filter(extract('month', events.date) == datetime.date.today().month,
                                extract('day', events.date) == datetime.date.today().day).all()
    if result != []:
        event = "It's\n"
        for thing in result:
            event = event + thing.name + ' (' + thing.date.strftime('%d/%m/%Y') + ')' + "\n"
    else:
        event = ""
    return(event)

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
        save_birthday(detail)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Birthday added!")
        )
    elif command == '/event':
        detail = event.message.text.split(' ')[1:]
        save_event(detail)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Event added!")
        )
    elif command == '/today':
        bday = todaybday()
        events = todayevent()
        if bday == "" and event == "":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Nothing Today")
            )
        elif bday != "" and events == "":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=bday)
            )
        elif bday == "" and events != "":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=events)
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=(bday+"\n"+events))
            )

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
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
    config("5r5JMAD8idgh2/+xLvMJljc/6y60VEdqfAG1ghjkMCPPutBR+TbbW7ym8cE4UV5ew0sSsLJyOteTVF+FZ581vHkcDuenLfdxorjKb2GoJNPd270iL688WspS8Zp/tLCAML+l2u63z8W3Ev6e9ijGHgdB04t89/1O/w1cDnyilFU=",
           default=os.environ.get('5r5JMAD8idgh2/+xLvMJljc/6y60VEdqfAG1ghjkMCPPutBR+TbbW7ym8cE4UV5ew0sSsLJyOteTVF+FZ581vHkcDuenLfdxorjKb2GoJNPd270iL688WspS8Zp/tLCAML+l2u63z8W3Ev6e9ijGHgdB04t89/1O/w1cDnyilFU='))
)
# get LINE_CHANNEL_SECRET from your environment variable
handler = WebhookHandler(
    config("eea0c199a2535f0c8f8db1e2ffcfc979",
           default=os.environ.get('eea0c199a2535f0c8f8db1e2ffcfc979'))
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
    if event.message.text == "hai":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="hullo")
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )



if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
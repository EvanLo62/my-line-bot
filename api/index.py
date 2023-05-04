from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('UNqrgdVFsi5OPdNsyy6H3zp5tkJqPquCDcS596bgU1tggL9n60QUam8ZQQQqdgAkvPqZpKugnAqN6N5Id11xiMRq7ynRmg3n/AdYpqpw3w2bGx8eNo03kqS6iN0ZIzxRgmEH4Zasny2lfQyY4TZxUAdB04t89/1O/w1cDnyilFU=')
webhook_handler = WebhookHandler('2c61617dd7275afc7127ec4c280b02a5')

@app.route("/")
def home():
    return "Line Bot API Server is Running"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        webhook_handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@webhook_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
import openai
import os

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

def chatgpt(input):
    # 設定 OpenAI API 密鑰
    openai.api_key = os.environ["OPENAI_API_KEY"]
    # openai.api_key = "OPENAI_API_KEY"

    # 設定 GPT-3.5 模型的檢索引擎
    model_engine = "text-davinci-003"

    # 設定生成的文本長度
    output_length = 300

    input_text = input

        # 使用 GPT-3.5 模型生成文本
    response = openai.Completion.create(
        engine=model_engine,
        prompt=input_text,
        max_tokens = output_length,
    )

    return response.choices[0].text

app = Flask(__name__)

line_bot_api = LineBotApi('qJtCt4QbX76HjLUY/BpU/+bahr/G4TnH8EVCgOaIgQu5spEYzrwBSm7oE2LYEQeEvPqZpKugnAqN6N5Id11xiMRq7ynRmg3n/AdYpqpw3w24LTOVn7wNUDlmSnu+eyipaT722a2o7P9pMoug1eEMrwdB04t89/1O/w1cDnyilFU=')
webhook_handler = WebhookHandler('8d5ad769bf3db12f5a7a56728bd7c0b7')


@app.route("/")
def home():
    return "LINE BOT API Server is running."

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
        TextSendMessage(text=chatgpt(event.message.text)))

if __name__ == "__main__":
    app.run()
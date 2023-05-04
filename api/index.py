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

app = Flask(__name__)

line_bot_api = LineBotApi('WnOAh83Ss4qSMw/6INKsbJnAdHS7Xe8T7qMRJ4bPwrzIEzkRezQDM2ow3KFjsQYqp2YHyvqOAaGdhFllhKLqjkEcRK8Kl/SBjqBGM+9SwDbaeQNahdjrp0TpsK6S3U32kwsr/4YVxTnH9O4nAUFySwdB04t89/1O/w1cDnyilFU=')
webhook_handler = WebhookHandler('4a02436c986b12d55a812b590e515f96')

# 設定 OpenAI API 密鑰
openai.api_key = os.environ["OPENAI_API_KEY"]
# openai.api_key = "OPENAI_API_KEY"

# 設定 GPT-3.5 模型的檢索引擎
model_engine = "text-davinci-003"

# 設定生成的文本長度
output_length = 300


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

    # 使用 GPT-3.5 模型生成文本
    response = openai.Completion.create(
        engine=model_engine,
        prompt=event.message.text,
        max_tokens=output_length,
    )

    # 取得生成的文本
    output_text = response.choices[0].text.strip()

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=output_text))


if __name__ == "__main__":
    app.run()
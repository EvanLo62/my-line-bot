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

    # 設定OpenAI API密鑰
    openai.api_key = os.environ["OPENAI_API_KEY"]

    # 載入ChatGPT模型
    model_engine = "text-davinci-003"

    # 設定使用者輸入
    input_text = input

    # 設定生成的文本長度
    output_length = 300

    # 生成回應
    # response = model.complete(prompt, max_tokens=100)
    response = openai.Completion.create(
        engine=model_engine,
        prompt=input_text,
        max_tokens=output_length,
    )

    # 輸出回應
    return response.choices[0].text

app = Flask(__name__)

line_bot_api = LineBotApi('ntH7w+oaDQpKyx9A2cLVQJeF8AquXIbMk9emJGhuyv1qSELTficcRjFNrtVmK4Ff2t9W1TfOMR8HQ0DATg1E2ZSAq3OKiq/kmTU0hePhfw7DZ74PSgkRtw3BmzTncQA5GRoQbscVCpwVs8IkSpcwygdB04t89/1O/w1cDnyilFU=')
webhook_handler = WebhookHandler('cd438be337f0423b8afcd5326a37e615')

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

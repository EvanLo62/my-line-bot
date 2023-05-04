import openai
import os

# 設定 OpenAI API 密鑰3
openai.api_key = os.environ["OPENAI_API_KEY"]

# 輸入文本
input_text = "今天天氣很好，請用中文回答。請做一首跟天氣有關的詩"

# 設定 GPT-3.5 模型的檢索引擎
model_engine = "text-davinci-003"

# 設定生成的文本長度
output_length = 300

# 使用 GPT-3.5 模型生成文本
response = openai.Completion.create(
    engine=model_engine,
    prompt=input_text,
    max_tokens=output_length,
)

# 取得生成的文本
output_text = response.choices[0].text.strip()

# 印出生成的文本
print(output_text)

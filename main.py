from flask import Flask, request, abort
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
from urllib.parse import urlparse
from database import MyDatabase

from seleniumbase import Driver
from selenium.webdriver.common.by import By
import json

from collections import defaultdict
def is_valid_url_from_domain(url, domain='https://m.happymh.com'):
    try:
        # 解析 URL
        parsed_url = urlparse(url)
        # 檢查是否有網絡協議（scheme），通常是http或https
        # 檢查網絡位置部分（netloc）是否包含特定域名
        if parsed_url.scheme in ['http', 'https'] and domain in parsed_url.geturl():
            return True
        else:
            return False
    except ValueError:
        # 如果 URL 格式錯誤，urlparse 可能會拋出 ValueError
        return False

def get_info(url):
    driver = Driver(uc=True, headless=True)
    driver.get(url)
    script_tags = driver.find_elements(By.XPATH, "//script[@type='application/json']")
    info = defaultdict()
    info['code'] = url.split('/')[-1]
    for script_tag in script_tags:
        json_text = script_tag.get_attribute('textContent')
        try:
            data = json.loads(json_text)
            if "serie_name" in data:
                info['name'] = data["serie_name"]
            
            if "praiseForm" in data:
                info['score'] = data['score']
                info['latest_ch_id'] = data['limitList'][0]['id']
                info['latest_ch_name'] = data['limitList'][0]['chapterName']
        except json.JSONDecodeError:
            continue 
    driver.quit()   
    return info

# 初始化 Flask 應用和 LINE Bot API
app = Flask(__name__)
configuration  = Configuration(access_token='2KczDjE9Fzunj9vniYy3uc4DHdnUyjji+uTt9ClBpjTX04+FoKHIxB2BA3ODdFZBhEg2FAr8QYvIM50UUzyByVpMHgIBv+FomMvquk30ga0d7N9BedDervhr0ymC71o5rNtRdiCx7v6KHkm4WuWoeQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('af5b659f25e80d5495cd6b0b978c3189')

# 定義路由來處理 Webhook
@app.route("/callback", methods=['POST'])
def callback():
    # 獲取 X-Line-Signature 頭用於驗證
    signature = request.headers['X-Line-Signature']

    # 獲取 POST 請求的主體
    body = request.get_data(as_text=True)

    # 處理 Webhook 主體
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

# 處理文字訊息
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        text = event.message.text
        if is_valid_url_from_domain(text):
            comic_info = get_info(text)
            db = MyDatabase()
            status_msg = db.insert_data(comic_info)
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=status_msg)]
            )
        )

if __name__ == "__main__":
    app.run()

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# 初始化 Flask 應用和 LINE Bot API
app = Flask(__name__)
line_bot_api = LineBotApi('ypI6rx3vsD0+ARZoF2vgKHp3+4pFMquP/Q85y7a9Qtzgnd3rZnh/k2ivua70K41PhEg2FAr8QYvIM50UUzyByVpMHgIBv+FomMvquk30ga3hF4Shm3C+hG3f8OjWQBa0i26ePiwhFL+Xloxg4pl7nQdB04t89/1O/w1cDnyilFU=')  # 替換為你的 Channel Access Token
handler = WebhookHandler('af5b659f25e80d5495cd6b0b978c3189')  # 替換為你的 Channel Secret

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
        abort(400)

    return 'OK'

# 處理文字訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text

    if text == 'bookcase':
        base_url = 'https://m.happymh.com'
        username = 'howard022619@gmail.com'
        password = '1234567890'
        
        driver = uc.Chrome(headless=True, service_args=["--verbose", "--log-path=cd.log"])
        wait = WebDriverWait(driver, 10)
        print("========== driver open ==========")
        login_url = os.path.join(base_url, 'user/login')
        driver.get(login_url)
        print(driver.page_source)
        driver.save_screenshot('my_screenshot.png')
        driver.close()

        '''
        driver.find_element(By.ID, 'email').send_keys(username)
        driver.find_element(By.ID, 'password').send_keys(password)

        login_button = driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-default[type="submit"]')
        login_button.click()
        wait.until(EC.url_changes(login_url))

        bookcase_url = os.path.join(base_url, 'bookcase')
        driver.get(bookcase_url)
        wait.until(EC.url_changes(base_url))

        booklist = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.booklist#books'))
        )

        print(booklist.is_displayed())
        print(booklist.get_attribute('outerHTML'))

        time.sleep(10)

        manga_info_list = []

        manga_list = driver.find_elements(By.CSS_SELECTOR, "#books div[role='listitem']")

        for manga in manga_list:
            manga_url = manga.find_element(By.TAG_NAME, "a").get_attribute("href")
            manga_name = manga.find_element(By.CLASS_NAME, "manga-title").text
            manga_chapter = manga.find_element(By.CLASS_NAME, "manga-chapter").text.split('/')
            
            manga_info_list.append(f"{manga_name}, {manga_chapter[0]}/{manga_chapter[1]}, {manga_url}")

        manga_info_str = "\n".join(manga_info_list)
        print(manga_info_str)
        driver.close()

        reply_message = TextSendMessage(text=manga_info_str)
        line_bot_api.reply_message(event.reply_token, reply_message)
        '''
if __name__ == "__main__":
    app.run()

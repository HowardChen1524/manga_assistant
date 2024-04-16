from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from seleniumbase import Driver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time


base_url = 'https://m.happymh.com'
username = 'howard022619@gmail.com'
password = '1234567890'

# driver = uc.Chrome(headless=True, service_args=["--verbose", "--log-path=cd.log"])
# driver = uc.Chrome()
driver = Driver(uc=True, headless=True)
wait = WebDriverWait(driver, 10)
print("========== driver open ==========")
login_url = os.path.join(base_url, 'user/login')
driver.get(login_url)
# print(driver.page_source)
# driver.save_screenshot('my_screenshot.png')
# driver.close()

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

# print(booklist.is_displayed())
# print(booklist.get_attribute('outerHTML'))

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
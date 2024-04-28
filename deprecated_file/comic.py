from seleniumbase import Driver
from selenium.webdriver.common.by import By
import json


''' 
TODO: Concept flow
1. Get spec comic info
2. Add to database
3. Get database comic
4. For each comic, check update status
5. if update, insert to reply list
'''
class ComicInformation():
    def __init__(self, url):
        self.base_url = ''.join(url.split('/')[:-2])
        self.code = url.split('/')[-1]
        self.get_info(url)
    
    def get_info(self, url):
        driver = Driver(uc=True, headless=True)
        driver.get(url)
        script_tags = driver.find_elements(By.XPATH, "//script[@type='application/json']")
        for script_tag in script_tags:
            json_text = script_tag.get_attribute('textContent')
            try:
                data = json.loads(json_text)
                if "serie_name" in data:
                    self.name = data["serie_name"]
                
                if "praiseForm" in data:
                    self.score = data['score']
                    self.latest_ch_id = data['limitList'][0]['id']
                    self.latest_ch_name = data['limitList'][0]['chapterName']

            except json.JSONDecodeError:
                continue
    
    def show_info(self):
        return "漫畫名: {}, 評分: {}, 最近更新: {}".format(self.name, self.score, self.latest_ch_name)
        
if __name__ == "__main__":
    ex_url = 'https://m.happymh.com/manga/lanxiang'
    comic = ComicInformation(ex_url)
    print(comic.show_info())
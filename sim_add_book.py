from urllib.parse import urlparse
from database import MyDatabase

from seleniumbase import Driver
from selenium.webdriver.common.by import By
import json
import time
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

def sim_add_book(text):
    if is_valid_url_from_domain(text):
        comic_info = get_info(text)
        db = MyDatabase()
        status_msg = db.insert_data(comic_info)
        print(status_msg)
    else:
        print("Wrong URL")
    

if __name__ == "__main__":
    # text = str(input("Please enter comic url: "))
    comic_list = [r'https://m.happymh.com/manga/silingshushixueyuandezhaohuantiancai',
                  r'https://m.happymh.com/manga/huanyingjiaruchaoyuezhexueyuan',
                  r'https://m.happymh.com/manga/quanyuanaomijia',
                  r'https://m.happymh.com/manga/guaishou8hao',
                  r'https://m.happymh.com/manga/yirenzhixia',
                  r'https://m.happymh.com/manga/xiaobafuzeren',
                  r'https://m.happymh.com/manga/sishenpiaoyue',
                  r'https://m.happymh.com/manga/jiongturensheng2',
                  r'https://m.happymh.com/manga/tianmoyucheng',
                  r'https://m.happymh.com/manga/yiwangzhilizhongsheng',
                  r'https://m.happymh.com/manga/daiwangraoming',
                  r'https://m.happymh.com/manga/SSSjikuangzhanshihuigui',
                  r'https://m.happymh.com/manga/heiyuz2his3hen',
                  r'https://m.happymh.com/manga/2dengwushen',
                  r'https://m.happymh.com/manga/kanlianshidai',
                  r'https://m.happymh.com/manga/zuijianyexing',
                  r'https://m.happymh.com/manga/fanpaijsuesha2342',
                  r'https://m.happymh.com/manga/kuangmozhongsheng',
                  r'https://m.happymh.com/manga/huangjiaxueyuandetiancaijianhao',
                  r'https://m.happymh.com/manga/woshihuaixiaozi',
                  r'https://m.happymh.com/manga/rujiantongxuerumole',
                  r'https://m.happymh.com/manga/baipazhanshen',
                  r'https://m.happymh.com/manga/gujiantongxueshigoutonglushe',
                  r'https://m.happymh.com/manga/manjiwanjiadedi100cihuigui',
                  r'https://m.happymh.com/manga/shaonianyongbing',
                  r'https://m.happymh.com/manga/zhainandalanqiu',
                  r'https://m.happymh.com/manga/moutianchengweimoshen',
                  r'https://m.happymh.com/manga/nvpengyoujiewoyixia',
                  r'https://m.happymh.com/manga/BLUELOCK',
                  r'https://m.happymh.com/manga/WINDBREAKER',
                  r'https://m.happymh.com/manga/baiXX',
                  r'https://m.happymh.com/manga/dianjuren',
                  r'https://m.happymh.com/manga/congdiyuguilaideshengzuo',
                  r'https://m.happymh.com/manga/monvyushimo',
                  r'https://m.happymh.com/manga/xingjiahunjiangchuan',
                  r'https://m.happymh.com/manga/cengjingshizuizhongBOSS',
                  r'https://m.happymh.com/manga/xingjiandashi',
                  r'https://m.happymh.com/manga/miewangzhihoudeshijie',
                  r'https://m.happymh.com/manga/mofaxueyuandeweizhuangjiaoshi',
                  r'https://m.happymh.com/manga/youxizuiqiangjiaojuzhe',
                  r'https://m.happymh.com/manga/lanxiang',
                  r'https://m.happymh.com/manga/woshalexueyuanwanjia',
                  r'https://m.happymh.com/manga/chaoziranwuzhuangdangdadang911',
                  r'https://m.happymh.com/manga/tiancaiwanjia',
                  r'https://m.happymh.com/manga/dingjiyingxiongguilai',
                  r'https://m.happymh.com/manga/SSSjizishalieren',
                  r'https://m.happymh.com/manga/renwuzhishangzhuyi',
                  r'https://m.happymh.com/manga/shashouzhuanzhi',
                  r'https://m.happymh.com/manga/huodeshenhuajiwupin',
                  r'https://m.happymh.com/manga/woduzimanjixinshou',
                  r'https://m.happymh.com/manga/kewangfuchoudezuiqiangyongzheyiheianzhilisuoxiangpimi',
                  r'https://m.happymh.com/manga/zhuangbeiwozuiqiang',
                  r'https://m.happymh.com/manga/yeyingjiadedazuozhan',
                  r'https://m.happymh.com/manga/banbenDAYS',
                  r'https://m.happymh.com/manga/tesheGAGAGA',
                  r'https://m.happymh.com/manga/jianzunguilai',
                  r'https://m.happymh.com/manga/yitongluanshi',
                  r'https://m.happymh.com/manga/wonengfuzhitianfu',
                  r'https://m.happymh.com/manga/buyaoqifuwozhangjingtongxue',
                  r'https://m.happymh.com/manga/wodeyingxiongxueyuan',
                  r'https://m.happymh.com/manga/youzhiyuanWARS',
                  r'https://m.happymh.com/manga/fufuyishanglianrenweiman',
                  r'https://m.happymh.com/manga/wopeiyangdeSjimen',
                  r'https://m.happymh.com/manga/zaichaoshihoumenxiyandeerren',
                  r'https://m.happymh.com/manga/xinwangqiuwangzi',
                  r'https://m.happymh.com/manga/zhongshengzuiqiangwanjia',
                  r'https://m.happymh.com/manga/huanyinggansidui',
                  r'https://m.happymh.com/manga/zhongshengbuliangshaojiaozhu',
                  r'https://m.happymh.com/manga/kexuechaodiancipao',
                  r'https://m.happymh.com/manga/MYHOMEHERO',
                  r'https://m.happymh.com/manga/ruguobuxiangsi',
                  r'https://m.happymh.com/manga/fuchutiangoudesanxiongdi',
                  r'https://m.happymh.com/manga/gengyirenouzhuiruaihe',
                  r'https://m.happymh.com/manga/ezhifuchou',
                  r'https://m.happymh.com/manga/AcmaGame142',
                  r'https://m.happymh.com/manga/shiling',
                  r'https://m.happymh.com/manga/emobianhusuo',
                  r'https://m.happymh.com/manga/wushenhuiguilu',
                  r'https://m.happymh.com/manga/BLAME',
                  r'https://m.happymh.com/manga/GSmeishen',
                  r'https://m.happymh.com/manga/xianshirenwu',
                  r'https://m.happymh.com/manga/wanglimofaxueyuandeliedengsheng',
                  r'https://m.happymh.com/manga/dixiachengfuchouji',
                  r'https://m.happymh.com/manga/silingfashizhongshengdewoquanjinengjingtong',
                  r'https://m.happymh.com/manga/BADTHINKINGDIARY',
                  r'https://m.happymh.com/manga/jianshumingmendexiaoerzi',
                  r'https://m.happymh.com/manga/zuiqiangxiaohao',
                  r'https://m.happymh.com/manga/doushenzhuanshengji',
                  r'https://m.happymh.com/manga/Upgradealone',
                  r'https://m.happymh.com/manga/diercizouxianghongtan',
                  r'https://m.happymh.com/manga/pizixueba',
                  r'https://m.happymh.com/manga/gelaipunier',
                  r'https://m.happymh.com/manga/jianyuleyuan',
                  r'https://m.happymh.com/manga/zhaomingshangdian',
                  r'https://m.happymh.com/manga/100',
                  r'https://m.happymh.com/manga/ruguoAItongzhishijie',
                  r'https://m.happymh.com/manga/LOCKEROPENERquanmianjiesuo']
    for b in comic_list:
        sim_add_book(b)
        time.sleep(5)
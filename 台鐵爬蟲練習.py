import requests
from bs4 import BeautifulSoup
import time

                                        #寫在前面
                                        #   ↓---------內文-------↓ 
                                        #<p>My cat is very grumpy.</p>
                                        # ↑開頭標籤                ↑結尾標籤
                                        #↑-----------元素------------↑
                                        #<p class: "editor-none">My cat is very grumpy.</p>
                                        #   ↑------屬性--------↑


                                        #find_all。find_all會將所有滿足條件的值取出，組成一個list。
                                        #find_all（標籤, 屬性, 遞歸, 文本, 限制, 關鍵詞）

url = 'https://www.railway.gov.tw/tra-tip-web/tip';
nameForStationAndID = {};
today = time.strftime('%Y/%m/%d').lstrip('0');
sTime = '06:00' 
eTime = '12:00'
print(today)
                                        #字典。鍵值對應、可變(mutable)的資料型態，沒有順序性。
                                        #key:value
                                        #example = {key1:value1. key2:value2}
                                        #key必須為不可變的資料型態，通常使用字串。value為可變或不可變的資料型態都可以。

                                        #movie = {'name':'Saving Private Ryan', #電影名稱
                                        #'year':1998, #電影上映年份
                                        #director':'Steven Spielberg',#導演
                                        #'Writer': 'Robert Rodat', #編劇
                                        #'Stars':['Tom Hanks', 'Matt Damon', 'Tom Sizemore'],#明星
                                        #'Oscar ':['Best Director','Best Cinematography','Best Sound','Best Film Editing','Best Effects, Sound Effects Editing']
                                        #獲得的奧斯卡獎項
                                        #}
                                        #另一個例子↓
                                        #desserts = {'Muffin':39, 'Scone':25, 'Biscuit':20}
def twRailWay():
    response = requests.get(url);
    if response.status_code != 200:
        print('URL發生錯誤:' + url)

    soup = BeautifulSoup(response.text, 'html5lib');
    stations = soup.find(id = 'cityHot').ul.find_all('li')
                                        #↑直接寫.ul，表find()
    for station in stations:
        stationName = station.button.text; #找到車站名稱。
        stationID = station.button['title']; #車站代碼。使用[]取得屬性的值。
        nameForStationAndID[stationName] = stationID #建立車站名稱對應車站代碼的字典。

    csrf = soup.find(id = 'queryForm').find('input',{'name':'_csrf'})['value']
    formDate = {
            'trainTypeList' : 'ALL',
            'transfer' : 'ONE',
            'startOrEndTime' : 'true',
            'startStation' : nameForStationAndID['臺北'],
            'endStation' : nameForStationAndID['新竹'],
            'rideDate' : today,
            'startTime' : sTime,
            'endTime' : eTime
    }

    queryUrl = soup.find(id='queryForm')['action'];
    qResp = requests.post('https://tip.railway.gov.tw/tra-tip-web/tip'+queryUrl, date=formDate);
#↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑建置準備傳給網站的表單↑↑↑↑↑↑幹，好麻煩↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
    qSoup = BeautifulSoup(qResp.text, 'html5lib');
#----以下照打
    trs = qSoup.find_all('tr', 'trip-column');
    for tr in trs:
        td = tr.find_all('td')
        print('%s : %s, %s' % (td[0].ul.li.a.text, td[1].text, td[2].text))

twRailWay()

#適逢台鐵網頁改版，pending
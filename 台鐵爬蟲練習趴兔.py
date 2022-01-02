import requests;
from bs4 import BeautifulSoup;
import time

url = 'https://www.railway.gov.tw/tra-tip-web/tip';
dictOfStationAndCode = {}; #車站名稱與車站代碼會匯入到這個字典，以key-value的方式。 車站名稱被標籤button包了起來。
today = time.strftime('%Y/%m/%d');
starTime = '06:00';
endTime = '12:00';

def action():
    resp = requests.get(url);
    if resp.status_code != 200:
        print('URL發生錯誤: '+url);
        return

    soup = BeautifulSoup(resp.text, 'html5lib');
    stations = soup.find(id = 'cityHot').ul.find_all('li');
    for station in stations: #用station這個變數名稱，表示所有找到的li元素。
        stationName = station.button.text; #將標籤button元素轉為字串。
        stationID = station.button['title']; #車站代碼。標籤button中的屬性title。[]取得屬性中的值。
        dictOfStationAndCode[stationName] = stationID #將車站名稱放在字典變數中的key。
#取得CSRF代碼。位於id名稱為queryForm的標籤裡面。
    csrf = soup.find(id='queryForm').find('input',{'name':'_csrf'})['value'] #裡頭有個input，屬性name為_csrf的標籤。
#↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑要傳送出去的表單↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
    fromDate = { #要回傳的表單是字典型態的變數。
        'trainTypeList':'All', #三個固定的資料?不是變數。
        'transfer':'ONE',
        'startOrEnTime': 'true',
        'startStation':dictOfStationAndCode['基隆'],
        'endStation':dictOfStationAndCode['臺北'],
        'rideDate': today,
        'startTime': starTime,
        'endTime': endTime,
    };
#form表單中，有一個屬性action。其提供傳送表單的網址，故要先找到這串網址的資訊。
    queryUrl = soup.find(id = 'queryForm')['action'];
    qResp = requests.post('https://www.railway.gov.tw'+queryUrl, data = fromDate); #用來傳送表單查詢車次的網址
    qSoup = BeautifulSoup(qResp.text, 'html5lib'); 
    trs = qSoup.find_all('tr', 'trip-column ') #回傳後的車次清單，是放在標籤tr，屬性trip-column中。 用find_all找到每一列車次資料，並用for迴圈取出標籤tr代表一列車次的所有資料。 
    for tr in trs:
        td = tr.find_all('td'); #其中又有多個標籤td，將資料一欄一欄的區隔開。 需再次使用find_all找出所有標籤td的元素。
        print('%s : %s, %s' % (td[0].ul.li.a.text, td[1].text, td[2].text)) #列印出格式依序為 車種車次、出發時間、抵達時間 三種資訊的內容。 
        #標籤td中尚有子標籤，依序為ul, li及a。故依序往下搜索，然後取得字串。
action()

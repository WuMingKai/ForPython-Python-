import requests
from bs4 import BeautifulSoup
import time #時間模組

today = time.strftime('%m/%d').lstrip('0') #取得今天的時間字串。 .lstrip可以把05、04等左邊的0移除。
print(today)

def pttNBA(url):
    response = requests.get(url);
    if response.status_code != 200:
        print('URL發生錯誤:' + url)
        return

    soup = BeautifulSoup(response.text, 'html5lib');
    ##.find().find_all()
    #find完element後，再針對element進行find_all()的動作
    #例如:soup.find("table").find_all("tr")
    #找到table標籤底下的所有tr標籤
    #注意不可寫成.find_all().find()
                                                                    #↓可以直接取得元素中屬性的資料。
    paging = soup.find('div', 'btn-group-paging').find_all('a')[1]['href']; 
                                                               #↑由於上一頁的連結在第二個(第一項)，所以取得索引值為1的資料。
    #上述執行緒仍是相對位置，下方在寫執行緒時還需要再加上PTT的網域名稱。
    articles = [] #宣告一個變數 articles，下方符合條件的文章，都會依序放在這個變數裡面。
    rents = soup.find_all('div', 'r-ent');
    for rent in rents:
                                             #↓去掉空白字元。
        title = rent.find('div', 'title').text.strip();                    #取得每一列文章的標題。
        count = rent.find('div', 'nrec').text.strip();                     #取得文章的推文數。
        date  = rent.find('div', 'meta').find('div','date').text.strip(); #取得文章的日期。因日期被包覆，所以要用兩個find。
        article = '%s %s:%s' %(date, count, title);

        try:
            if today == date and int(count) > 10:
                articles.append(article);
        except:
            if today == date and count == '爆':
                articles.append(article);
    if len(articles) != 0:
        for article in articles:
            print(article)
        pttNBA('https://www.ptt.cc' + paging);
    else:
        return
pttNBA('https://www.ptt.cc/bbs/NBA/index.html')

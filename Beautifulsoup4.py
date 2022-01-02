import requests
from bs4 import BeautifulSoup

                                        #寫在前面
                                        #   ↓---------內文-------↓ 
                                        #<p>My cat is very grumpy.</p>
                                        # ↑開頭標籤                ↑結尾標籤
                                        #↑-----------元素------------↑
                                        #<p class: "editor-none">My cat is very grumpy.</p>
                                        #   ↑------屬性--------↑

url = requests.get('https://code-gym.github.io/spider_demo/')
soup = BeautifulSoup(url.text, 'html5lib') #.text 表示要取得response中的文字內容。html5lib是種分析器。此行將url的回傳結果，交給BeautyfulSoup做解析。

                                        #find。只能找單一元素，可回傳成text或str屬性

print(soup.find('h1')) #尋找網頁中第一個h1標籤的元素
#<h1>Code Gym 爬蟲教學</h1>
print(soup.find('h1').text) #尋找網頁中第一個h1標籤的內文
#Code Gym 爬蟲教學
print(soup.h1) #尋找網頁中第一個h1標籤的元素
#<h1>Code Gym 爬蟲教學</h1>
print(soup.h1.text) #尋找網頁中第一個h1標籤的內文
#Code Gym 爬蟲教學

                                        #find_all。find_all會將所有滿足條件的值取出，組成一個list。
                                        #find_all（標籤, 屬性, 遞歸, 文本, 限制, 關鍵詞）

for h3 in soup.find_all('h3'):
    print(h3.string)

print('----分隔線----')
for h3 in soup.find_all('h3'):#Html中有超連結，使用 a 開頭標籤。
    print(h3.a)

#亦可用標籤中的屬性(Attribute)來查找

print('===分隔線===')
for titleAsClass in soup.find_all('h3','post-title'):
    print(titleAsClass.a.text) #若使用屬性+超連結a的找法，原本印出時會出現的「none」，都會消失。
print('||||||||分|||||||||||||||||||||||||||||隔|||||||||||||||||||||||||||||||||線|||||||||||||||')
#當網頁中的標籤不只一種的時候，可以尋找多種標籤。使用key-value。
for doubleCategory in soup.find_all('a',{'class':'post-category','class':'cat-1'}): #尋找全部標籤中帶有a，且屬性為「post-category」及「cat-1」的元素
    print(doubleCategory.text)

print('以下練習') #使用Beautifulsoup中的stripped_strings，將空白的部分省略，不印出來。回傳的是generator物件

for work in soup.find_all('div', 'post-body'): 
    print(work)
print('!!!!!!!!!!!!!!!!!!!!!!!!!!!分隔線')
for workToUseStrippedStrings in soup.find_all('div','post-body'):
    for works in workToUseStrippedStrings.stripped_strings:
        print(works)

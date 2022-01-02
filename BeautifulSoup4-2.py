import requests
from bs4 import BeautifulSoup

url = requests.get('https://code-gym.github.io/spider_demo/');
soup = BeautifulSoup(url.text,'html5lib'); 

#欲取得header中所有的程式碼
idNav = soup.find(id = 'nav');
allContent = idNav.parent;
print(allContent)

#如何尋找平行的姊妹節點
#先找到標籤名稱 li，屬性class為cat-2的javascript選項
print('分隔線')
for fINd in soup.find_all('li','cat-2'):
    print(fINd.text);
    print(fINd.previous_sibling.text);
    print(fINd.next_sibling.text)

#找子節點
print('分隔線')
for ul in soup.find_all('ul'):
    for li in ul.children:
        for xd in li.stripped_strings:
            print(xd)

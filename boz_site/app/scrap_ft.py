import requests
from bs4 import BeautifulSoup as bs
import os
dir_path=os.path.dirname(os.path.realpath(__file__))

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
}

url = 'https://odibets.com/booklet'
page=requests.get(url,headers=headers)
cd_page=bs(page.content,'html.parser')
data=cd_page.find_all('td')
os.system("echo '' > game.txt")
for td_tag in data:
        print(td_tag.get_text(strip=True))
        lines=(td_tag.get_text(strip=True))
        os.system(f'echo """{lines}""" >> game.txt')
           
os.system("sed -i '1,8d' game.txt")
os.system(f"grep -v '/' game.txt > {dir_path}/../media/shell_scripts/use.txt")

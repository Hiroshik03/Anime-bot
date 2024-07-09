from bs4 import BeautifulSoup
import requests
import fake_useragent
class champ_stats():
    CS = 0
    KDA =0.0
    winrate =0
    games =0
class champ(champ_stats):
    def __init__(self,name):
        self.name = name
    name ="" 
class sumoner_info():
    champs = []
    nick =""
    icon_url =""
    level = 0
    rank =""
    rank_icon =""
    winrate =""
    win_lose =""

async def find(region,name,tag):
    data = sumoner_info()
    user = fake_useragent.UserAgent().random
    HEADERS2 = {'User_Agent': user}
    response1 = requests.get(f"https://www.op.gg/summoners/{region}/{name}-{tag}",  headers = HEADERS2, ).text
    soup = BeautifulSoup(response1, 'html.parser')
    data.nick = soup.find('strong', class_ = 'css-ao94tw e1swkqyq1').text
    data.icon_url = soup.find('div', class_ = 'profile-icon').find('img').attrs['src'].split('?')[0]
    data.rank = soup.find('div', class_ = 'tier').text
    data.level = int(soup.find('span', class_ = 'level').text)
    data.winrate = soup.find('div', class_ = 'ratio').text
    data.win_lose = soup.find('div',class_ = "win-lose").text
    data.rank_icon = f"https://opgg-static.akamaized.net/images/medals_new/{data.rank.split(' ')[0]}.png"
    return data
#data.champs.append(champ())
#print(data.rank_icon)
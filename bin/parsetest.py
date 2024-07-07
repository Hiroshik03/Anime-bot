from bs4 import BeautifulSoup
import requests
import fake_useragent
user = fake_useragent.UserAgent().random
HEADERS2 = {'User_Agent': user}
response1 = requests.get("https://animego.org/anime/zvezdnoe-ditya-2-2605",  headers = HEADERS2, ).text
soup = BeautifulSoup(response1, 'html.parser')
data=[]
try:
    trailer = soup.find('a', class_ = 'video-item position-relative d-flex lazy').attrs['href']
except:
    trailer ="None"
try:
    series = soup.find_all('dd', class_='col-6 col-sm-8 mb-1')[1].text
except:
    series ="None"
full_descrioption = soup.find('div', class_='description pb-3').text
anonce = soup.find('dd', class_= 'col-12 col-sm-8 mb-1').text
data.append([trailer,series,full_descrioption,anonce])
print(trailer)
print(series)
print(full_descrioption)
print(anonce)


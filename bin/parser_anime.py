from selenium import webdriver as wd
from selenium.webdriver.common.by import By
import time
import anime_db
# data reader
async def data_reader():
    data = []
    # browser properties
    options = wd.ChromeOptions()
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36")
    browser = wd.Chrome(
        options=options
    )
    # Parse data
    browser.get("https://animego.org")
    update_list = browser.find_elements(By.ID, "slide-toggle-1")
    update_list = update_list[0].find_elements(By.CLASS_NAME, 'last-update-item')
    for child in update_list:
        series = child.find_element(By.CLASS_NAME, "ml-3").text
        name = child.find_element(By.CLASS_NAME, "last-update-title").text
        png = child.find_element(By.CLASS_NAME,"img-square").get_attribute("style")[23:116]
        data.append([name,series,png])
    browser.quit()
    return data
async def data_reader_on_year(year):
    data = []
    options = wd.ChromeOptions()
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36")
    browser = wd.Chrome(
        options=options
    )
    browser.get("https://animego.org/anime/season/"+str(year)+"?sort=r.rating&direction=desc")
    lenOfPage = browser.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match = False
    while (match == False):
        lastCount = lenOfPage
        time.sleep(2)
        lenOfPage = browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount == lenOfPage:
            match = True
    update_list = browser.find_elements(By.CLASS_NAME, "col-12")
    for child in update_list:
        if(child.text == ""):
            continue
        browser.execute_script("window.scrollTo(0,"+str(child.location['y'])+");")
        url = child.find_element(By.TAG_NAME,"a").get_attribute('href')
        name = child.find_element(By.CLASS_NAME,"h5").text
        png = child.find_element(By.CLASS_NAME,"anime-list-lazy").get_attribute("data-original")
        try:
            genre = child.find_element(By.CLASS_NAME,"anime-genre").text
        except:
            genre = "Не определен"
        dicription = child.find_element(By.CLASS_NAME,"description").text
        try:
            raiting = child.find_element(By.CLASS_NAME,"p-rate-flag__text").text
        except:
            raiting ="NO"
        description = child.find_element(By.CLASS_NAME,"description").text
        data.append([name,url,png,raiting,description,genre,dicription])
    await anime_db.anime_on_year_set(data,year)
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=chrome_options)

url = 'https://lex.uz/uz/search/unique'
driver.get(url)

urls = []
with open('urls.csv', 'a+', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['url'])

    while True:
        soupx = BeautifulSoup(driver.page_source, 'html.parser')

        for a in soupx.find_all('a', {'class' : 'lx_link'}):
            writer.writerow(['https://lex.uz'+a['href']])

        try:
            element = driver.find_element(By.ID, "ucFoundActsControl_LinkButton1")
            element.click()
        except:
            break
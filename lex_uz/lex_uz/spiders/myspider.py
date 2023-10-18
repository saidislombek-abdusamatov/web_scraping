import scrapy
from bs4 import BeautifulSoup

class MyspiderSpider(scrapy.Spider):
    name = "myspider"
    allowed_domains = ["lex.uz"]
    base_url = "https://lex.uz"
    start_urls = ['https://lex.uz/uz/search/unique']

    def parse(self, response):
        with open("urls.csv", "r") as file:
            for url in file.read().split()[1:]:
                yield response.follow(url, callback=self.parse_detail)

    def parse_detail(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            from_ = soup.find('div', class_="ACCEPTING_BODY").text.strip()+' '+soup.find('div', class_="ACT_FORM").text.strip()
        except:
            from_ = soup.find('div', class_="ACT_FORM").text.strip()
        title = soup.find('div', class_="ACT_TITLE").text.strip()
        content = soup.find('div', class_="docBody__container").text.strip()
        
        yield {
            'from':from_,
            'title':title,
            'content':content
        }
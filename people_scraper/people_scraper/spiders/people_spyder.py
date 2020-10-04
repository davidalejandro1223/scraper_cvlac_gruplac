import scrapy
import pandas as pd
import unicodedata

class PeopleScrapy(scrapy.Spider):
    name = 'people'

    def start_requests(self):
        df = pd.read_excel("urlsInvestigadores.xlsx")
        for index, row in df.iterrows():
            yield scrapy.Request(url=row['URL persona'], callback=self.parse)

    
    def parse(self, response):
        nombre = response.xpath('/html[1]/body[1]/div[1]/div[3]/table[1]/tr[2]/td[1]/table[1]/tr[3]/td[2]/text()').get()
        nombre = unicodedata.normalize('NFKD', nombre.strip())
        print(nombre)
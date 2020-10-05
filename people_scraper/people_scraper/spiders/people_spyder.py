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
        
        titulo = response.xpath('/html[1]/body[1]/div[1]/div[3]/table[1]/tr[3]/td[1]/table[1]/tr[2]/td[2]/text()').get()
        titulo = unicodedata.normalize('NFKD', titulo.strip())
        
        cvlac = response.url
        
        orcid = response.xpath('/html[1]/body[1]/div[1]/div[3]/table[1]/tr[2]/td[1]/table[1]/tr[7]/td[1]/a[1]/@href').get()
        if orcid is not None:
             orcid = unicodedata.normalize('NFKD',orcid.strip())
        
        investigador = response.xpath('/html[1]/body[1]/div[1]/div[3]/table[1]/tr[2]/td[1]/table[1]/tr[2]/td[2]/text()').get()
        investigador = unicodedata.normalize('NFKD', investigador.strip())
        
        areas = response.xpath('/html[1]/body[1]/div[1]/div[3]/table[1]/tr[6]/td[1]/table[1]')
        areas_actuacion = []
        for area in areas:
            actuacion = area.xpath('tr/td[1]/li[1]/text()').getall()
            areas_actuacion = map(lambda x: unicodedata.normalize('NFKD',x.strip()),actuacion)
        

        yield {
            'nombre':nombre,
            'cvlac':cvlac,
            'titulo':titulo,
            'orcid':orcid,
            'investigador':investigador,
            'areas_actuacion':list(areas_actuacion)
        }
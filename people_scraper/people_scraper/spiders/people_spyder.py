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
        
        tabla_intro = response.xpath('/html[1]/body[1]/div[1]/div[3]/table[1]/tr[2]/td[1]/table/tr')
        for item in tabla_intro:
            nom_col = item.xpath('td[1]/text()').get()
            nom_orcid = item.xpath('td[1]/a/text()').get()
            print(nom_col)
            if nom_col=='Nombre':
                nombre = item.xpath('td[2]/text()').get()
                nombre = unicodedata.normalize('NFKD', nombre.strip())
            if nom_col=='Categoría':
                try:
                    investigador = item.xpath('td[2]/text()').get()
                    investigador = unicodedata.normalize('NFKD', investigador.strip())
                except:
                    investigador = None
            if nom_orcid is not None and nom_orcid=='Código ORCID':
                orcid = item.xpath('td[1]/a/@href').get()
                orcid = unicodedata.normalize('NFKD',orcid.strip())
            else:
                orcid = None

        
        titulo = response.xpath('/html[1]/body[1]/div[1]/div[3]/table[1]/tr[3]/td[1]/table[1]/tr[2]/td[2]/text()').get()
        titulo = unicodedata.normalize('NFKD', titulo)
        
        cvlac = response.url       
        
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
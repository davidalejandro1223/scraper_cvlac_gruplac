import scrapy
import pandas as pd
import unicodedata

class Gruplac(scrapy.Spider):
    name = "gruplac"
    def start_requests(self):
        df = pd.read_excel("urlsInvestigadores.xlsx")
        df=df.dropna(axis=0, how='any')
        print(df['URL grupo'])
        for index, row in df.iterrows():
            print(row)
            yield scrapy.Request(url=row['URL grupo'], callback=self.parse)

    def parse(self, response):
        lider = response.xpath('/html[1]/body[1]/table[1]/tr[4]/td[2]/text()').get()
        lider = unicodedata.normalize('NFKD', lider.strip())
        nombre = response.xpath('/html[1]/body[1]/span[1]/text()').get()
        nombre = unicodedata.normalize('NFKD', nombre.strip())
        gruplac = response.url
        pagina = response.xpath('/html[1]/body[1]/table[1]/tr[6]/td[2]/a[1]/text()').get()
        pagina = unicodedata.normalize('NFKD', pagina.strip())
        clasificacion = response.xpath('/html[1]/body[1]/table[1]/tr[8]/td[2]/b[1]/text()').get()
        if clasificacion is not None:
            clasificacion = unicodedata.normalize('NFKD', clasificacion.strip())
        
        correo = response.xpath('/html[1]/body[1]/table[1]/tr[7]/td[2]/a[1]/text()').get()
        correo = unicodedata.normalize('NFKD', correo.strip())
        lineas = response.xpath('/html[1]/body[1]/table[4]')
        lineasinv = []

        for linea in lineas:
            inv = linea.xpath('tr/td[1]/text()').getall()
            lineasinv = map(lambda x: unicodedata.normalize('NFKD',x.strip()),inv)
        
        lineasinv = list(lineasinv)
        #print(nombre)
        #print(gruplac)
        #print(pagina)
        #print(clasificacion)
        #print(lineasinv)
        #print(correo)
        
        yield {
            'lider':lider,
            'nombre':nombre,
            'gruplac':gruplac,
            'pagina':pagina,
            'clasificacion':clasificacion,
            'correo':correo,
            'lineasinv':list(lineasinv)
        }
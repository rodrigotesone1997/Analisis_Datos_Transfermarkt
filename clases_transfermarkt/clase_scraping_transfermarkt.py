import requests
from bs4 import BeautifulSoup
from requests.api import head


class scraping_transfermarkt:
    def scraper_jugadores(url):
        pass
    def scraper_transferencias(self, url):
        
        headers = {'User-Agent': 'placeholder'}
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find('table', class_='items')
        body = table.find('tbody')
        for child in body.contents:
            if child.name:
                print(child.name)
        # rows = body.find_all('tr')

        salida = dict.fromkeys([
            'url_imagen',
            'nombre_completo',
            'posicion',
            'edad',
            'nacionalidad',
            'equipo_abandonado',
            'nacionalidad_equipo_abandonado',
            'nacionalidad_equipo_unido',
            'equipo_ingresado',
            'fee',
        ])
        
        return salida


    def scraper_empresas(url):
        pass

url_transf = r'https://www.transfermarkt.com/transfers/neuestetransfers/statistik/plus/?plus=1&galerie=0&wettbewerb_id=alle&land_id=&minMarktwert=0&maxMarktwert=200.000.000&yt0=Show'

scraper = scraping_transfermarkt()
scraper.scraper_transferencias(url_transf)
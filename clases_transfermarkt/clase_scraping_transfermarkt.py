import requests
from bs4 import BeautifulSoup
from requests.api import head

from pprint import pprint

class scraping_transfermarkt:
    def scraper_jugadores(url):
        pass
    def scraper_transferencias(self, url):
        
        keys =[
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
            ]

        headers = {'User-Agent': 'placeholder'}
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find('table', class_='items')
        body = table.find('tbody')

        transfers_list = []

        for i, row in enumerate(body.contents):
            # Ignoramos filas None
            if row.name:

                transfer = dict.fromkeys(keys)

                columns = row.contents
                '''Cada columna tiene un estilo especial, extraemos los datos de a una
                '''
                player = columns[1]
                tds = player.find_all('td')

                url_imagen = tds[0].find('img')['data-src']
                transfer['url_imagen'] = url_imagen

                nombre_completo = tds[1].find('a').text
                transfer['nombre_completo'] = nombre_completo

                posicion = tds[2].text
                transfer['posicion'] = posicion
                
                age = columns[2]
                transfer['edad'] = int(age.text)

                nationality = columns[3]
                nats = [flag['title'] for flag in nationality.find_all('img')]
                transfer['nacionalidad'] = nats

                left = columns[4]
                team_elem = left.find('td', class_='hauptlink')
                equipo_ab = team_elem.find('a').text
                transfer['equipo_abandonado'] = equipo_ab
                
                # No podemos tomar el pais del texto, ya que en algunos casos es el
                # nombre de la liga. Lo extraemos de la imagen de la bandera.
                pais_ab = left.find('img', class_='flaggernrahmen')['title']
                transfer['nacionalidad_equipo_abandonado'] = pais_ab

                joined = columns[5]
                team_elem = joined.find('td', class_='hauptlink')
                equipo_un = team_elem.find('a').text
                transfer['equipo_unido'] = equipo_un
                
                pais_un = joined.find('img', class_='flaggernrahmen')['title']
                transfer['nacionalidad_equipo_unido'] = pais_un

                
                tr_date = columns[6]
                mkt_value = columns[7]
                fee = columns[8]
                pprint(transfer)

                transfers_list.append(transfer)
            if i==1:
                break
        
        return transfers_list


    def scraper_empresas(url):
        pass

url_transf = r'https://www.transfermarkt.com/transfers/neuestetransfers/statistik/plus/?plus=1&galerie=0&wettbewerb_id=alle&land_id=&minMarktwert=0&maxMarktwert=200.000.000&yt0=Show'

scraper = scraping_transfermarkt()
scraper.scraper_transferencias(url_transf)
import requests
from bs4 import BeautifulSoup

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
                'equipo_unido',
                'fecha_transferencia',
                'valor_mercado',
                'fee',
            ]

        transfers_list = []

        headers = {'User-Agent': 'placeholder'}
        try:
            page = requests.get(url, headers=headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            table = soup.find('table', class_='items')

            body = table.find('tbody')

            for row in body.contents:
                # Ignoramos filas None
                if not row.name: continue
    
                transfer = dict.fromkeys(keys)
    
                columns = row.contents
                #Cada columna tiene un estilo especial, extraemos los datos de a una
                
                player = columns[1]
                tds = player.find_all('td')
    
                url_foto = tds[0].find('img')['data-src']
                transfer['url_imagen'] = url_foto
    
                nombre_completo = tds[1].find('a').text
                transfer['nombre_completo'] = nombre_completo
    
                posicion = tds[2].text
                transfer['posicion'] = posicion
                
                age = columns[2]
                edad = int(age.text) if age.text.isdigit() else None
                transfer['edad'] = edad
    
                nationality = columns[3]
                nats = [flag['title'] for flag in nationality.find_all('img')]
                transfer['nacionalidad'] = nats
    
                left = columns[4]
                team_elem = left.find('td', class_='hauptlink')
                equipo_or = team_elem.find('a').text
                transfer['equipo_abandonado'] = equipo_or
                
                # No podemos tomar el pais del texto, ya que en algunos casos es el
                # nombre de la liga. Lo extraemos de la imagen de la bandera. 
                # Algunos nombres de paises pueden estar en aleman.
                pais_or_elem = left.find('img', class_='flaggenrahmen')
                # Además, cuando el pais de origen o llegada es "Without club", no 
                # tengo pais
                pais_or = pais_or_elem['title'] if pais_or_elem else None
                transfer['nacionalidad_equipo_abandonado'] = pais_or
    
                joined = columns[5]
                team_elem = joined.find('td', class_='hauptlink')
                equipo_un_elem = team_elem.find('a')
                # Ademas de las consideraciones para los paises, cuando el equipo de 
                # llegada es "Retired", el elemento no es un link, y tengo que contarlo
                # por separado
                equipo_un = equipo_un_elem.text if equipo_un_elem else 'Retirado'
                transfer['equipo_unido'] = equipo_un
                
                pais_un_elem = joined.find('img', class_='flaggenrahmen')
                pais_un = pais_un_elem['title'] if pais_un_elem else None
                transfer['nacionalidad_equipo_unido'] = pais_un
    
                tr_date = columns[6]
                transfer['fecha_transferencia'] = tr_date.txt
    
                mkt_value = columns[7]
                transfer['valor_mercado'] = mkt_value.text
    
                fee = columns[8]
                transfer['fee'] = fee.find('a').text
                # text, _, money = fee.partition('€')
                # if money:
                #     fee = self.convert_currency_float(money)
                # else:
                #     fee = text
                # transfer['fee'] = fee

                transfers_list.append(transfer)
        except AttributeError:
            print("No hay elementos disponibles en este url\n")
        return transfers_list

    # def convert_currency_float(self, text):
    #     if text.endswith('Th.'):
    #         multiplier = 1000
    #         n = 3
    #     elif text.endswith('m'):
    #         multiplier = 1_000_000
    #         n = 1
    #     else:
    #         raise ValueError('No puedo convertir este valor')

    #     value = float(text[:-n])
    #     return value*multiplier

    def scraper_empresas(url):
        pass

if __name__ == '__main__':

#    url_transf = r"https://stackoverflow.com/questions/52051989/requests-exceptions-connectionerror-connection-aborted-connectionreseterro"
#    url_transf = r"https://www.transfermarkt.com/transfers/neuestetransfers/statistik/plus/?plus=1&galerie=0&wettbewerb_id=IT1&land_id=1&minMarktwert=0&maxMarktwert=200.000.000&yt0=Show"
#    url_transf = r"https://www.transfermarkt.com/transfers/neuestetransfers/statistik/plus/?plus=1&galerie=0&wettbewerb_id=IT1&land_id=&minMarktwert=0&maxMarktwert=200.000.000&yt0=Show"
    url_transf = r'https://www.transfermarkt.com/transfers/neuestetransfers/statistik/plus/?plus=1&galerie=0&wettbewerb_id=alle&land_id=9&minMarktwert=0&maxMarktwert=200.000.000&yt0=Show'

    scraper = scraping_transfermarkt()
    transferencias = scraper.scraper_transferencias(url_transf)

    pprint(transferencias)
from bs4 import BeautifulSoup
import requests


class scraping_transfermarkt:
    def __init__(self):
        pass
    def scraper_jugadores(self,url):

        # TODO: Hacer las keys de url_icono_de_banderas y url_icono_de_redes_sociales y añadir sus values

        # Algunas llaves estan repetidas pero no importan porque los diccionarios NO permiten tener llaves repetidas
        # y se encargan de sobreescribir los datos repetidos sin crear llaves nuevas 
        keys_list = [
                    'Nombre', 'Fecha de Nacimiento', 'Lugar de Nacimiento', 'Edad',
                    'Altura', 'Nacionalidad', 'Posición', 'Pie dominante', 'Agente', 'Club Actual', 
                    'Inicio de Contrato', 'Finalización de su Contrato', 'Patrocinador', 'Redes Sociales', 'Redes Sociales', 
                    'Url_current_club', 'Club Actual', 'Liga', 'Nivel de Liga', 'Inicio de Contrato', 'Finalización de su Contrato',
                    'Fecha de Nacimiento', 'Lugar de Nacimiento', 'Nacionalidad', 'Altura', 
                    'Posición', 'Finalización de su Contrato', 'Situación Internacional', 'Cap/Goals',
                    'Valor de Mercado', 'Última Revisión del Valor de Mercado'
                    ]
        #Lista para almacenar los valores que obtengamos
        values_list = []


        # Los headers nos ayudan a que el sitio web no rechaze nuestras solicitudes
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0'}
        response = requests.get(url, headers=headers)
        # Obtenemos el texto de nuestra peticion 
        content = response.text
        soup = BeautifulSoup(content, 'lxml')

        """ 
        Primera Tabla  

        De esta tabla obtendremos estos datos: 

        data =  [
                'Nombre', 'Fecha de Nacimiento', 'Lugar de Nacimiento', 'Edad',
                'Altura', 'Nacionalidad', 'Posición', 'Pie dominante', 'Agente',
                'Club Actual', 'Inicio de Contrato', 'Finalización de su Contrato', 
                'Patrocinador', 'Redes Sociales'
                ]
           
        """

        # Primera tabla de los datos del jugador
        first_table = soup.find('div', class_='info-table info-table--right-space')

        # En data_player almacenamos todos los dataValue de los datos del jugador de la tabla principal
        data_player = first_table.find_all('span', class_='info-table__content info-table__content--bold')

        for info in data_player:
            # Esto remplaza "\xa0m" por m(metros), del campo edad
            ordered_info = info.text.strip().replace('\xa0m', 'm')
            values_list.append(ordered_info)

    


        # Buscamos todos las etiquetas <a> de la first tabla
        all_links_first_table = first_table.find_all('a')
        # Lista que almacenara todos los links de manera general
        links = []
        # Lista que almacenaran los links de sus redes sociales 
        social_media_list = []
        # El url del current_club que esta en el codigo fuente viene sin el protocolo https y sin el url inicial
        # de la homepage, el url que nos da el scraping es como este: 'fc-paris-saint-germain/startseite/verein/583'
        # Usaremos la lista para almacenar el url con el protolo https del home y el url dado del scraping
        https_with_url = ['https://www.transfermarkt.com']

        for link in all_links_first_table:
            # Agregamos cada link a la lista links
            links.append(link['href'])
        """ 
        Estos son todos las url que estaran en la lista links
        ['/aktuell/waspassiertheute/aktuell/new/datum/1998-12-20', 
        '/fc-paris-saint-germain/startseite/verein/583', 
        '/fc-paris-saint-germain/startseite/verein/583', 'http://twitter.com/KMbappe',
        'http://www.facebook.com/kylianmbappeofficiel/', 'http://www.instagram.com/k.mbappe/']

        Urls que filtraremos, para traer solo las urls que nos interesan.
        Iteraremos sobre esta lista y mediante su indice escogemos los datos que necesitamos

         """
        
        for i in range(2,6):
            if i == 2:
                # Añadiremos el url del current club a la lista https_with_club
                https_with_url.append(links[i])
            else:
                # Añadiremos los links de las redes sociales a social_media_list
                social_media_list.append(links[i])
        # Agregamos la lista con los links de las redes sociales
        values_list.append(social_media_list)
        # Unimos el url del home page con el url dado del scraping que contiene el link current_club
        url_current_club = ''.join(https_with_url)
        # Agregamos el link de su club actual
        values_list.append(url_current_club)
        
        

        """ 
        Segunda Tabla 
        
        De esta tabla obtendremos estos datos:
        
        data = ['Club Actual', 'Liga', 'Nivel de Liga', 'Inicio de Contrato', 'Finalización de su Contrato']

        """
        
        # Segunda Tabla con los datos del jugador
        second_table = soup.find('div', class_='dataZusatzDaten')

        # Informacion sobre el nombre de su equipo y su liga
        league_and_team = second_table.find_all('a')
        for info in league_and_team:
            ordered_info = info.text.strip()
            # Agregamos los datos a nuestra lista
            values_list.append(ordered_info)
       
        # Informacion de su contrato y nivel de liga
        contractinfo_leaguelvl = second_table.find_all('span', class_='dataValue')
        # Iteramos para extraer los datos
        for info in contractinfo_leaguelvl:
            ordered_info = info.text.strip()
            # Agregamos los datos a nuestra lista
            values_list.append(ordered_info)



        """ 
        Tercera Tabla  
        
        De esta tabla obtendremos estos datos:

        data = [
                'Fecha de Nacimiento', 'Lugar de Nacimiento', 'Nacionalidad', 'Altura', 
                'Posición', 'Finalización de su Contrato', 'Situación Internacional', 'Cap/Goals'
                ]
        """ 
    
        # Tercera Tabla con los datos del jugador
        third_table = soup.find_all('div', class_='dataDaten')
        # Esta tabla tiene 3 divs llamados dataDaten por lo que iteramos sobre ellos
        for dataDaten in third_table:
            spans = dataDaten.find_all('span', class_='dataValue')
            # Iteramos por los spans que tienen los divs 
            for span in spans:
                # El replace soluciona un bug
                ordered_info = span.text.strip().replace('                                                                            (22)', '')
                values_list.append(ordered_info)


        
        """ 
        Cuarta Tabla 

        De esta tabla obtendremos estos datos:
        
        data = ['market_value', 'last_update_market_value']

        En este pedazo de código obtenemos valores como estos:
        [0]Valor de mercado actual: 160,00 mill. €
        [1]Última revisión: 01/06/2021
        [2]Valor más alto: 200,00 mill. € 17/12/2018

        """

        # Creamos una lista vacia que recibira todos los datos mencionados en la parte de arriba,
        # de los cuales solo necesitaremos los valores con indice [0] y [1]
        market_list = []
        # Cuarta Tabla con los datos del jugador
        fourth_table = soup.find('div', class_='large-5 columns small-12')
        market_values = fourth_table.find_all('div', class_='right-td')
        for market_value in market_values:
            market_list.append(market_value.text.strip())
        # Ya que solo necesitamos el valor de mercado actual y su ultima revision
        # Solo agregamos esos valores a la values_list
        values_list.append(market_list[0])
        values_list.append(market_list[1])
        
        
        """ 
        Aca tendremos el diccionario con los datos del jugador
        Cuyo diccionario con los datos del jugador se vera asi

        Ejemplo:

        mydict = {Nombre: Messi, Edad: 38, ...}
        
        """
        # En este diccionario se almacenaran los datos del jugador
        final_data_player = {}
        # Unimos las llaves con las valores que scrapeamos
        zip_iterator = zip(keys_list, values_list)
        # Convertimos la unión de las listas en un diccionario y lo almacenamos en el 
        # diccionario final_data_player
        final_data_player = dict(zip_iterator)
        print(final_data_player)

    def scraper_transferencias(url):
        pass
    def scraper_empresas(url):
        pass

if __name__ == '__main__':
    url = 'https://www.transfermarkt.com/kylian-mbappe/profil/spieler/342229'
    player = scraping_transfermarkt()
    player.scraper_jugadores(url)
    


from bs4 import BeautifulSoup
import requests


class scraping_transfermarkt:
    def __init__(self):
        pass
    def scraper_jugadores(self,url):

        keys = [
            # PRIMERA TABLA
            'Name',
            'Date of Birth',
            'Place of Birth',
            'Age',
            'Height',
            'Citizenship',
            'Position',
            'Foot',
            'Player Agent',
            'Current Club',
            'Joined',
            'Contract Expired',
            'Contract Option',
            'Outfitter',
            'Social Media',
            'Social Media Icons',
            'Flags Icons',
            # SEGUNDA TABLA
            'Current Club Link',
            'League',
            'League Level',
            # TERCERA TABLA
            'Market Value',
            'Last Update Market Value'
        ]
        # Creando el diccionario
        player_info = dict.fromkeys(keys)

        headers = {'User-Agent': 'placeholder'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')

        """ 
        PRIMERA TABLA  

        De esta tabla obtendremos estos datos: 

        data =  [
                'Nombre', 'Fecha de Nacimiento', 'Lugar de Nacimiento', 'Edad',
                'Altura', 'Nacionalidad', 'Posición', 'Pie dominante', 'Agente',
                'Club Actual', 'Inicio de Contrato', 'Finalización de su Contrato', 
                'Patrocinador', 'Redes Sociales'
                ]
           
        """
        # Almacenara todos los valores de data_player
        values_list = []

        # PRIMERA TABLA de los datos del jugador
        first_table = soup.find('div', class_='large-6 large-pull-6 small-12 columns spielerdatenundfakten')

        # En data_player almacenamos todos los dataValue de los datos del jugador de la tabla principal
        data_player = first_table.find_all('span', class_='info-table__content info-table__content--bold')

        # Iteramos sobre la primera tabla y agregamos los valores a values_list
        # FIXME: Aca surge la duda ya que los datos de la primera tabla no tienen un patron 
        # en especifico, en algunos casos tienen los 15 o 14 datos en otros solo tienen 4 o 9
        # Como desarrollar un patron o metodo que se encarge de esto
        try:
            for info in data_player:
                # Esto elimina los \xa0 del código
                ordered_info = info.text.strip().replace('\xa0', ' ')
                values_list.append(ordered_info)

            name = values_list[0]
            player_info['Name'] = name

            birth_date = values_list[1]
            player_info['Date of Birth'] = birth_date

            place_of_birth = values_list[2]
            player_info['Place of Birth'] = place_of_birth

            age = int(values_list[3])
            player_info['Age'] = age

            height = values_list[4].replace(',', '.')
            player_info['Height'] = float(height.replace(' m', ''))

            citizenship = values_list[5].split() 
            player_info['Citizenship'] = citizenship

            position = values_list[6]
            player_info['Position'] = position

            dominant_foot = values_list[7]
            player_info['Foot'] = dominant_foot

            player_agent = values_list[8]
            player_info['Player Agent'] = player_agent

            current_club = values_list[9]
            player_info['Current Club'] = current_club

            commencement_date = values_list[10]
            player_info['Joined'] = commencement_date 

            contract_expired = values_list[11]
            player_info['Contract Expired'] = contract_expired
            # NOTA: Esto del if lo aplique porque pense que solo el contract option era el que variaba
            # Si el len de lista es 15 significa que tiene contract_option
            if len(values_list) == 15:
                contract_option = values_list[12]
                player_info['Contract Option'] = contract_option

                outfitter = values_list[13]
                player_info['Outfitter'] = outfitter if outfitter else None
            # Si el len de lista es 14 significa que no tiene contract_option
            else:
                outfitter = values_list[12]
                player_info['Outfitter'] = outfitter if outfitter else None

        except IndexError:
            print('El indice a buscar no existe')


        # LINKS DE LA PRIMERA TABLA
        links_list = []
        link_images_list = []
        # El div que contiene las redes sociales
        social_media_links = first_table.find('div', class_='socialmedia-icons')
    
        for link in social_media_links.find_all('a'):
            # Url de las redes sociales
            links_list.append(link['href'])
            # Url de los iconos de las redes sociales
            link_images_list.append(link.img['data-src'])
    
        player_info['Social Media'] = links_list
        player_info['Social Media Icons'] = link_images_list

        # Banderas de la primera Tabla
        flags = []
        url_flags = first_table.find_all('img', class_='flaggenrahmen')
        
        for flag in url_flags:
            # Filtra las imagenes de los gifts
            if 'https://' in flag['src']:
                flags.append(flag['src'])
        
        player_info['Flags Icons'] = flags
        """ 
        SEGUNDA TABLA 
        De esta tabla obtendremos estos datos:
        data = [Current Club Link', 'League', 'League Level']
        """

        # SEGUNDA TABLA con los datos del jugador
        second_table = soup.find('div', class_='dataZusatzDaten')
        league_and_team = second_table.find_all('span')

        # Completamos la url incompleta que nos da la página
        link = second_table.find('a')['href']
        url = ['https://www.transfermarkt.com', link]
        player_info['Current Club Link'] = ''.join(url)

        player_info['League'] = league_and_team[1].text.strip()
        player_info['League Level'] = league_and_team[3].text.strip()


        """ 
        TERCERA TABLA 
        De esta tabla obtendremos estos datos:
        data = ['market_value', 'last_update_market_value']
        """

        # TERCERA TABLA con los datos del jugador
        fourth_table = soup.find('div', class_='large-5 columns small-12')
        # Datos de los valores de mercado 
        market_values = fourth_table.find_all('div', class_='right-td')

        player_info['Market Value'] = market_values[0].text.strip()
        player_info['Last Update Market Value'] = market_values[1].text.strip()

        return player_info

    def scraper_transferencias(url):
        pass
    def scraper_empresas(url):
        pass

if __name__ == '__main__':
    #url = 'https://www.transfermarkt.com/lionel-messi/profil/spieler/28003'
    #url = 'https://www.transfermarkt.com/kylian-mbappe/profil/spieler/342229'
    #url = 'https://www.transfermarkt.com/junior-dina-ebimbe/profil/spieler/536482'
    url = 'https://www.transfermarkt.com/pape-cheikh/profil/spieler/336828'
    
    player = scraping_transfermarkt()
    datos_del_jugador = player.scraper_jugadores(url)
    print(datos_del_jugador)
    


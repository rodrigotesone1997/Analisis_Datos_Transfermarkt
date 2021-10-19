from bs4 import BeautifulSoup
import requests


class scraping_transfermarkt:
    def __init__(self):
        pass
    def scraper_jugadores(self,url):
        """
        Aún me falta agregar el contenido de las redes sociales, banderas y demas iconos,  
        también datos de la segunda y tercera tabla. Esto solo es una demostracion para la 
        PRIMERA TABLA
        Se aceptan consejos
        """
        keys = [
                # PRIMERA TABLA
                'Name in home country',
                'Date of birth',
                'Place of birth',
                'Age',
                'Height',
                'Citizenship',
                'Position',
                'Foot',
                'Player agent',
                'Current club',
                'Joined',
                'Contract option',
                'Contract expires',
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
        # Creo mi diccionario
        player_info = dict.fromkeys(keys)

        headers = {'User-Agent': 'placeholder'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')

        # PRIMERA TABLA
        first_table = soup.find('div', class_='large-6 large-pull-6 small-12 columns spielerdatenundfakten')
        # KEYS de la PRIMERA TABLA 
        data_regular = first_table.find_all('span', class_='info-table__content info-table__content--regular')
        # VALUES de la PRIMERA TABLA 
        data_bold = first_table.find_all('span', class_='info-table__content info-table__content--bold')

        # En algunas ocasiones no se encuentra el nombre del jugador en la primera tabla
        # por eso lo saco de otra seccion.
        player_name = soup.find('div', class_='dataName').h1
        player_info['Name in home country'] = player_name.text.strip()

        # Lista con las llaves de la primera table
        data_regs = []
        # Lista con los valores de la primera tabla
        data_bolds = []
        for info in data_bold:
            info = info.text.strip().replace('\xa0', ' ')
            data_bolds.append(info)

        for idx, data_reg in enumerate(data_regular):
            data_reg = data_reg.text.strip().replace(':', '')
            data_regs.append(data_reg)
            # Compruebo si un dato esta en la tabla iterando sobre las llaves de la primera tabla
            # si es así se agrega el dato, sino continua buscando, si no lo encuentra se queda en None
            try:
                if 'Date of birth' in data_regs[idx]:
                    # Si es su cumpleaños omitimos regresar la palabra Happy Birthday
                    player_info['Date of birth'] = data_bolds[idx].replace(' Happy Birthday', '')

                elif 'Place of birth' in data_regs[idx]:
                    player_info['Place of birth'] = data_bolds[idx]

                elif 'Age' in data_regs[idx]:
                    player_info['Age'] = int(data_bolds[idx])

                elif 'Height' in data_regs[idx]:
                    player_info['Height'] = float(data_bolds[idx].replace(',', '.').replace(' m', ''))

                elif 'Citizenship' in data_regs[idx]:
                    player_info['Citizenship'] = data_bolds[idx].split()

                elif 'Position' in data_regs[idx]:
                    player_info['Position'] = data_bolds[idx]

                elif 'Foot' in data_regs[idx]:
                    player_info['Foot'] = data_bolds[idx]

                elif 'Player agent' in data_regs[idx]:
                    player_info['Player agent'] = data_bolds[idx]
                    
                elif 'Current club' in data_regs[idx]:
                    player_info['Current club'] = data_bolds[idx] 

                elif 'Joined' in data_regs[idx]:
                    player_info['Joined'] = data_bolds[idx]

                elif 'Contract expires' in data_regs[idx]:
                    player_info['Contract expires'] = None if data_bolds[idx] == '-' else data_bolds[idx]

                elif 'Contract option' in data_regs[idx]:
                    player_info['Contract option'] = None if data_bolds[idx] == '-' else data_bolds[idx]  

                elif 'Outfitter' in data_regs[idx]:
                    player_info['Outfitter'] = None if data_bolds[idx] == '-' else data_bolds[idx]

            except IndexError:
                print('Error con el tope del indice')
            
             
        # LINKS DE LA PRIMERA TABLA
        # Url de las redes sociales
        links_list = []
        # Url de los iconos de las redes sociales
        link_images_list = []
        # El div que contiene las redes sociales
        try:
            social_media_links = first_table.find('div', class_='socialmedia-icons')
            
            for link in social_media_links.find_all('a'):
                links_list.append(link['href'])
                link_images_list.append(link.img['data-src'])
        
            player_info['Social Media'] = links_list
            player_info['Social Media Icons'] = link_images_list
        # Si no se encuentra el div con las redes sociales se quedan en None
        except:
            print('No se encontro la etiqueta div "socialmedia-icons" que contienen las redes sociales')
        
        # BANDERAS DE LA PRIMERA TABLA
        try:
            flags = []
            url_flags = first_table.find_all('img', class_='flaggenrahmen')
            
            for flag in url_flags:
                # Filtra las imagenes de los gifts
                if 'https://' in flag['src']:
                    flags.append(flag['src'])
            player_info['Flags Icons'] = flags
        except:
            # Si no existen los datos se quedan en None
            print('No se encontro la etiqueta img "flaggenrahmen" que contiene las banderas')



        # SEGUNDA TABLA
        second_table = soup.find('div', class_='dataZusatzDaten')
        try:
            current_link = second_table.find('span', class_='hauptpunkt')
            link = current_link.a['href'] if 'Retired' not in current_link.text else None
            # Completamos la url incompleta que nos da la página
            url = ['https://www.transfermarkt.com', link]
            player_info['Current Club Link'] = ''.join(url)

            league = second_table.find('span', class_='mediumpunkt')
            player_info['League'] = league.text.strip()

            data_value = second_table.find('span', class_='dataValue')
            data_item = second_table.find('span', class_='dataItem')
            player_info['League Level'] = data_value.text.strip() if 'League level:' in data_item.text else None

        except:
            # Si no existen los datos se quedan en None
            print('Algunos datos de la segunda tabla podrian estar vacios o inexistentes')
        


        # TERCERA TABLA
        fourth_table = soup.find('div', class_='large-5 columns small-12')
        # Datos de los valores de mercado
        try: 
            market_values = fourth_table.find_all('div', class_='right-td')
            market_value = market_values[0].text.strip()
            player_info['Market Value'] = None if market_value == '-' else market_value
            player_info['Last Update Market Value'] = market_values[1].text.strip()
        except:
            # Si no existen los datos se quedan en None
            print('Algunos datos de la tercera tabla podrian estar vacios o inexistentes')


        return player_info

if __name__ == '__main__':
    #url = 'https://www.transfermarkt.com/pape-cheikh/profil/spieler/336828'
    #url = 'https://www.transfermarkt.com/lionel-messi/profil/spieler/28003'
    #url = 'https://www.transfermarkt.com/zakaria-messibah/profil/spieler/416107'
    #url = 'https://www.transfermarkt.com/fabio-messi/profil/spieler/673358'
    #url = 'https://www.transfermarkt.com/jiri-krejci/profil/spieler/25595'
    #url = 'https://www.transfermarkt.com/javier-chevanton/profil/spieler/6420'
    url = 'https://www.transfermarkt.com/javier-zeoli/profil/spieler/258059'
    #url = 'https://www.transfermarkt.com/bandiougou-fadiga/profil/spieler/590914'
    player = scraping_transfermarkt()
    datos_del_jugador = player.scraper_jugadores(url)
    print(datos_del_jugador)
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
                'Social-Media'
        ]
        # Creo mi diccionario
        player_info = dict.fromkeys(keys)

        headers = {'User-Agent': 'placeholder'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')

        # PRIMERA TABLA
        first_table = soup.find('div', class_='large-6 large-pull-6 small-12 columns spielerdatenundfakten')
        # KEYS of THE FIRST TABLE
        data_regular = first_table.find_all('span', class_='info-table__content info-table__content--regular')
        # VALUES of THE FIRST TABLE
        data_bold = first_table.find_all('span', class_='info-table__content info-table__content--bold')

        # En algunas ocasiones no se encuentra el nombre del jugador en la primera tabla
        # por eso lo saco de otra seccion.
        player_name = soup.find('div', class_='dataName').h1
        player_info['Name in home country'] = player_name.text.strip()

        # Lista con los valores de la primera tabla
        data_bolds = []
        # Lista con las llaves de la primera table
        data_regs = []
        for info in data_bold:
            info = info.text.strip().replace('\xa0', ' ')
            data_bolds.append(info)

        for idx, data_reg in enumerate(data_regular):
            data_reg = data_reg.text.strip().replace(':', '')
            data_regs.append(data_reg)
            try:
                if 'Name in home country' in data_regs[idx]:
                    player_info['Name in home country'] = data_bolds[idx]

                elif 'Date of birth' in data_regs[idx]:
                    player_info['Date of birth'] = data_bolds[idx]

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

                elif 'Social-Media' in data_regs[idx]:
                    player_info['Social-Media'] = data_bolds[idx]
            except IndexError:
                print('Error con el tope del indice')
            
             

        return player_info

if __name__ == '__main__':
    url = 'https://www.transfermarkt.com/pape-cheikh/profil/spieler/336828'
    # url = 'https://www.transfermarkt.com/lionel-messi/profil/spieler/28003'
    # url = 'https://www.transfermarkt.com/zakaria-messibah/profil/spieler/416107'
    # url = 'https://www.transfermarkt.com/fabio-messi/profil/spieler/673358'
    player = scraping_transfermarkt()
    datos_del_jugador = player.scraper_jugadores(url)
    print(datos_del_jugador)

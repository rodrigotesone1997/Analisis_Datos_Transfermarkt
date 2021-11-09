from bs4 import BeautifulSoup
import requests

class scraping:
    def scraper_jugadores(url):
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
                    player_info['Age'] = data_bolds[idx]

                elif 'Height' in data_regs[idx]:
                    player_info['Height'] = data_bolds[idx].replace(',', '.').replace(' m', '')

                elif 'Citizenship' in data_regs[idx]:
                    player_info['Citizenship'] = ",".join(data_bolds[idx].split())

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
                    player_info['Contract expires'] = "" if data_bolds[idx] == '-' else data_bolds[idx]

                elif 'Contract option' in data_regs[idx]:
                    player_info['Contract option'] = "" if data_bolds[idx] == '-' else data_bolds[idx]  

                elif 'Outfitter' in data_regs[idx]:
                    player_info['Outfitter'] = "" if data_bolds[idx] == '-' else data_bolds[idx]

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
        
            player_info['Social Media'] = ",".join(links_list)
            player_info['Social Media Icons'] = ",".join(link_images_list)
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
            player_info['Flags Icons'] = ",".join(flags)
        except:
            # Si no existen los datos se quedan en None
            print('No se encontro la etiqueta img "flaggenrahmen" que contiene las banderas')



        # SEGUNDA TABLA
        second_table = soup.find('div', class_='dataZusatzDaten')
        try:
            current_link = second_table.find('span', class_='hauptpunkt')
            link = current_link.a['href'] if 'Retired' not in current_link.text else ""
            # Completamos la url incompleta que nos da la página
            url = ['https://www.transfermarkt.com', link]
            player_info['Current Club Link'] = ''.join(url)

            league = second_table.find('span', class_='mediumpunkt')
            player_info['League'] = league.text.strip()

            data_value = second_table.find('span', class_='dataValue')
            data_item = second_table.find('span', class_='dataItem')
            player_info['League Level'] = data_value.text.strip() if 'League level:' in data_item.text else ""

        except:
            # Si no existen los datos se quedan en None
            print('Algunos datos de la segunda tabla podrian estar vacios o inexistentes')



        # TERCERA TABLA
        fourth_table = soup.find('div', class_='large-5 columns small-12')
        # Datos de los valores de mercado
        try: 
            market_values = fourth_table.find_all('div', class_='right-td')
            market_value = market_values[0].text.strip()
            player_info['Market Value'] = "" if market_value == '-' else market_value
            player_info['Last Update Market Value'] = market_values[1].text.strip()
        except:
            # Si no existen los datos se quedan en None
            print('Algunos datos de la tercera tabla podrian estar vacios o inexistentes')


        return player_info


    def scraper_transferencias(url):

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
                edad = int(age.text) if age.text.isdigit() else ""
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
                pais_or = pais_or_elem['title'] if pais_or_elem else ""
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
                pais_un = pais_un_elem['title'] if pais_un_elem else ""
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
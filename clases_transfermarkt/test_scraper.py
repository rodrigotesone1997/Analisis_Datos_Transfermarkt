from bs4 import BeautifulSoup
import requests


# LISTA CON LAS PRINCIPALES LIGAS EUROPEAS DONDE SE PUEDE APLICAR EL SCRAPER
# Solo quitale el '#' a una url para activar el scrap en respectiva liga
# Premier League
# url = 'https://www.transfermarkt.com/premier-league/transfers/wettbewerb/GB1'
# Serie A
# url = 'https://www.transfermarkt.com/serie-a/transfers/wettbewerb/IT1'
# Ligue 1
# url = 'https://www.transfermarkt.com/ligue-1/transfers/wettbewerb/FR1'
# Bundesliga 
# url = 'https://www.transfermarkt.com/bundesliga/transfers/wettbewerb/L1'
# La Liga
url = 'https://www.transfermarkt.com/laliga/transfers/wettbewerb/ES1'

headers = {'User-Agent': 'placeholder'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Numero de jugadores extranjeros de cada liga
players_table = soup.find('table', class_='profilheader').contents
foreign_players = players_table[7].find('a').text.replace('Players', '')

# Nombre de liga
league_name = soup.find('div', id='wettbewerb_head').div.div.div.h1.text
# Identificador de banderas

column = soup.find('div', class_='large-8 columns')
# Un box esta compuesto por dos tablas
boxes = column.find_all('div', class_='box')
brasileros = []
argentinos = []
mkt_value_br = []
mkt_value_arg = []
age_br = []
age_arg = []
position_br = []
position_arg = []

# Recorremos todas las tablas que vienen en pares
for box in boxes[3:]:
    # Buscamos solo las tablas que contengan las imagenes las rp_tables
    r_tables = box.find_all('div', class_='responsive-table')
    for table in r_tables:
        # Por cada r_table nos quedaremos con las cuerpo de la tabla
        tbody = table.find('table').tbody
        # Nos quedamos con cada fila de la tabla
        rows = tbody.find_all('tr')
        # Por cada div que contenga la nacionalidad en cada fila
        for row in rows:
            # Imgs es la caja donde estan las imgs de las banderas
            imgs = row.find('td', class_='zentriert nat-transfer-cell')
            flags = imgs.find_all('img', class_='flaggenrahmen')
            # Estos comprehension estan medio raros, no se q hize pero funcionan. 
            # A petición los puedo quitar y hacerlos de la otra manera con mas sintaxis
            result_br = [ flag['title'] for flag in flags if flag['title'] == 'Brazil'] 
            if result_br:
                # Agregamos un brasilero a la lista
                brasileros.append(result_br)
                # Caja donde esta el valor de mercado de cada jugador
                # TODO: Usar la funcion de conversion de Saint para los market values.
                mkt_value = row.find('td', class_='rechts mw-transfer-cell').text
                mkt_value_br.append(mkt_value)
                age = row.find('td', class_='zentriert alter-transfer-cell').text
                age_br.append(age)
                position = row.find('td', class_='pos-transfer-cell').text
                position_br.append(position)
            
            
            result_arg = [flag['title'] for flag in flags if flag['title'] == 'Argentina']
            if result_arg: 
                # Agregamos un argentino a la lista
                argentinos.append(result_arg)
                # Caja donde esta el valor de mercado de cada jugador
                # TODO: Usar la funcion de conversion de Saint para los market values.
                mkt_value = row.find('td', class_='rechts mw-transfer-cell').text 
                mkt_value_arg.append(mkt_value)
                age = row.find('td', class_='zentriert alter-transfer-cell').text
                age_arg.append(age)
                position = row.find('td', class_='pos-transfer-cell').text
                position_arg.append(position)

            # BLOC DE NOTAS DEL SCRAPER
            #TODO: Iterar sobre la lista de los market values. Sacar un promedio y porcentaje
            # en base a la cantidad de jugadores argentinos y brasileros que existe en cada liga
            # y hacer una comparativa de market values. Tambien hacer una comparativa de que 
            # demografia es la preferida por cada liga respecto a los objetos interesados de estudio.
            # Ya tendriamos los datos solo faltaria filtrarlos y ponerlos en un diccionario u otro para
            # su mejor manejo y visualizacion
            # ----------------------------------------------------------------------------------------
            # Se aplicara selenium cuando el scraper este listo, ya que se usara para clickear entre
            # los botones de seleccion de liga. Y sera la manera mas efectiva de usarlo.


# PD. Todo esta a base de prints porque esta en fase de desarrollo xd
print(f'Número de jugadores extranjeros en la {league_name} : {int(foreign_players)}' )
print('De los cuales:')
print(f'- {len(brasileros)} son brasileros')
print(f'- {len(argentinos)} son argentinos')
print('Sus valores de mercado por nacionalidad son:')
print(f'Total br market values: {mkt_value_br}')
print(f'Total arg market values: {mkt_value_arg}')
print('Sus edades por nacionalidad son:')
print(f'Age br : {age_br}')
print(f'Age arg : {age_arg}')
print('Sus posiciones por nacionalidad son:')
print(f'Position br : {position_br}')
print(f'Position arg : {position_arg}')
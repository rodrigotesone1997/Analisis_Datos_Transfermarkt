from clases_transfermarkt import recoleccion_datos,scrapper_datos
import pandas as pd
if __name__=="__main__":
    # Aca prueban la implementacion de las funciones

    scrapper_jugadores=scrapper_datos.scraping.scraper_jugadores
    url="https://www.transfermarkt.com/lionel-messi/profil/spieler/28003"

    # Aca es una muestra de como pasar el diccionario a un archivo excel

    data=scrapper_jugadores(url)
    df=pd.DataFrame([data])

    df.to_excel("excel_prueba.xlsx",index=False)
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
import time



os.environ["PATH"] += r"C:/SeleniumDrivers"

class RecoleccionDatos:

    def price_difference(self):
        """ 
        Esta función comparara los precios de jugadores similares de distintos países
        PD: Elimine la funcion ya que al realizarlo con la funcion scraper_jugadores 
        sería mas tardio y tedioso dado los datos que queremos recolectar. Ya lo intente
        y creo encontrar el test_scraper mas eficaz para este caso
        """
        

recolector = RecoleccionDatos()
recolector.price_difference()
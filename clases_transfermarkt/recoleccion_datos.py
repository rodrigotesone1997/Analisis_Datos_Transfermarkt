from time import sleep

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from scrapper_datos import scraping


URL_TRANSFERENCIAS =r"https://www.transfermarkt.com/transfers/saisontransfers/statistik?plus=1"

class recoleccion_datos:

    def __init__(self):

        self.scraper = scraping()

        opts = Options()
        opts.headless = False  
        self.driver = Chrome(options=opts)
    
    def recolectar_transferencias(self):
        return self.driver
        


rd = recoleccion_datos()
driver = rd.recolectar_transferencias()


driver.get(URL_TRANSFERENCIAS)
sleep(3)
# Aceptar cookies
driver.switch_to.frame(1)
driver.find_element(By.CSS_SELECTOR, "button[title='ACCEPT ALL']").click()
driver.switch_to.parent_frame()

selects = driver.find_elements(By.TAG_NAME, "select")

Select(selects[0]).select_by_visible_text('19/20')
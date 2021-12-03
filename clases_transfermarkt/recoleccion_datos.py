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
        self.browser = Chrome(options=opts)
    
    def recolectar_transferencias(self):
        
        self.browser.get(URL_TRANSFERENCIAS)
        select = Select(self.browser.find_element(By.ID, "selUJM"))
        select.select_by_visible_text('19/20 ')


rd = recoleccion_datos()
rd.recolectar_transferencias()
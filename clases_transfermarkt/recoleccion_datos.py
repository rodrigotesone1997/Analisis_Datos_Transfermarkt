from time import sleep

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from scrapper_datos import scraping




class recoleccion_datos:

    URL_TRANSFERENCIAS =r"https://www.transfermarkt.com/transfers/saisontransfers/statistik?plus=1"

    def __init__(self):

        self.scraper = scraping()

        opts = Options()
        opts.headless = False  
        self.driver = Chrome(options=opts)
    

    def recolectar_transferencias(self, seleccion):
        
        self.driver.get(self.URL_TRANSFERENCIAS)
        sleep(3)
        # Aceptar cookies
        self.driver.switch_to.frame(1)
        self.driver.find_element(By.CSS_SELECTOR, "button[title='ACCEPT ALL']").click()
        self.driver.switch_to.parent_frame()

        select_divs = self.driver.find_elements(By.CLASS_NAME, "inline-select")

        
        # Elegir las opciones
        for sel_elem, sel in zip(select_divs, seleccion):
            sel_elem.click()
            input_field = sel_elem.find_element(By.TAG_NAME, 'input')
            input_field.send_keys(sel + Keys.RETURN)
        # Aceptar
        self.driver.find_element(By.CSS_SELECTOR, 'input[class="right button small"]').click() 
        sleep(3)

        print('primera hoja')
        data = self.scraper.scraper_transferencias(self.driver.current_url)
        print(len(data))
        next_page = self.driver.find_elements(
            By.CSS_SELECTOR, 
            'li[class="tm-pagination__list-item tm-pagination__list-item--icon-next-page"]'
            )

        n = 1
        while next_page:
            next_page[0].click()
            n +=1
            print(f"hoja numero {n}")
            sleep(7)
            # La URL no se actualiza al hacer click en siguiente, tengo que modificarla 
            # a mano. Igual paso de pagina para ver cuantas son
            url = self.driver.current_url + f"&page={n}"
            data.extend(self.scraper.scraper_transferencias(url))
            next_page = self.driver.find_elements(
                By.CSS_SELECTOR, 
                'li[class="tm-pagination__list-item tm-pagination__list-item--icon-next-page"]'
            )
        
        return data
        

        
        


if __name__ == '__main__':
    
    rd = recoleccion_datos()
    seleccion = [
        '19/20',
        'Sommertransfers',
        'All nationalities',
        'Goalkeeper',
        'All positions',
        'All age groups',
        'Only include loans',
    ]
    data = rd.recolectar_transferencias(seleccion)
    print(len(data)) #96
    


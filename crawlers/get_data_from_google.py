from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import re

class GoogleLocalScraper():

    def __init__(self):
        self.driver = None
        self.urls = []

    def set_urls(self, urls):
        self.urls = urls

    def scrape_data(self):
        for url in self.urls:
            self.driver.get(url)

            while True:
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.ykYNg > div'))
                    )
                    establishments = self.driver.find_elements(By.CSS_SELECTOR, 'div.ykYNg > div')

                    if not establishments:
                        break

                    for est in establishments:
                        try:
                            phone_spans = est.find_elements(By.CSS_SELECTOR, 'span.hGz87c')
                            phone_number = 'Telefone não disponível'

                            for span in phone_spans:
                                span_text = span.text
                                digits = re.findall(r'\d', span_text)
                                if len(digits) >= 8:
                                    phone_number = "".join(digits)
                                    break

                            establishment_name = est.find_element(By.CSS_SELECTOR, 'div.rgnuSb').text
                            data = {
                                'Nome': establishment_name,
                                'Telefone': phone_number
                            }
                            yield data
                        except NoSuchElementException:
                            continue

                    try:
                        next_button = self.driver.find_element(By.XPATH, '//button[@aria-label="Próxima"]')
                        if not next_button.is_displayed():
                            break
                        next_button.click()
                    except NoSuchElementException:
                        break
                except TimeoutException:
                    break

    def close_driver(self):
        if self.driver:
            self.driver.quit()

def funcao_main():
    urls = [
        "https://www.google.com/localservices/prolist?g2lbs=AP8S6EMVPDkPFmmWH0ug9_GMeqphsIC8aMwEdpr7oG70_KnEpvr-kDevADrLW4q4g_PzMsCFGMbNB1n6_RXmWr_qLKwUpEWOHhAdJs99YGXeH6uQiYs5AEXSNv2eoe3fAFzkwdL6H6y1&hl=pt-BR&gl=br&cs=1&ssta=1&oq=barbearia%20florianopolis&src=2&sa=X&sqi=2&q=barbearia%20florianopolis&ved=2ahUKEwjsnYvw1vuAAxV1r5UCHbhhDLkQjdcJegQIABAF&scp=ChBnY2lkOmJhcmJlcl9zaG9wEgAaACoJQmFyYmVhcmlh&slp=MgBAAVIECAIgAIgBAJoBBgoCFxkQAQ%3D%3D", 
        "https://www.google.com/localservices/prolist?g2lbs=AP8S6EPyPAUFx_u3AaDkoxat5faeSKWttD2jXveRqig17O42Tw3eoUEQUrKQZyn24oBDcN4dSuY8IG8Bk_Z9YG9RLVc9hKdArsdS7NER-NNBlj9DiclDHsUGJ-5iu35HMu9T4UGiSdBr&hl=pt-BR&gl=br&cs=1&ssta=1&oq=salao%20de%20beleza%20florianopolis&src=2&sa=X&q=loja%20de%20bebida%20florianopolis&ved=2ahUKEwjA6r_34_uAAxWbkpUCHbnICRgQjdcJegQIABAF&scp=CgpnY2lkOnN0b3JlEgAaACoETG9qYQ%3D%3D&slp=MgBAAVIECAIgAIgBAJoBBgoCFxkQAQ%3D%3D",
    ]
    chrome_options = Options()
    chrome_options.add_argument("--headless") 

    scraper = GoogleLocalScraper()
    scraper.set_urls(urls)

    with webdriver.Chrome(options=chrome_options) as driver:
        scraper.driver = driver
        for data in scraper.scrape_data():
            print(data)

if __name__ == "__main__":
    funcao_main()

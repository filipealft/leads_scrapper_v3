from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import re
import csv
import database

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
                            phone_number = ''

                            for span in phone_spans:
                                span_text = span.text
                                digits = re.findall(r'\d', span_text)
                                if len(digits) >= 11:
                                    phone_number = "".join(digits)
                                    break
                            if phone_number == '':
                                continue

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

def read_csv_urls(filename):
    urls = []
    with open(filename, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            urls.append(row['url'])
    return urls

def main_func():
    urls = database.fetch_urls_from_database()

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    scraper = GoogleLocalScraper()
    scraper.set_urls(urls)

    connection = database.connect_to_database()
    data_batch = []
    batch_size = 50 

    with webdriver.Chrome(options=chrome_options) as driver:
        scraper.driver = driver
        
        for url in urls:
            for data in scraper.scrape_data():
                print(data)
                data_batch.append((data['Nome'], data['Telefone']))

                if len(data_batch) == batch_size:
                    database.batch_insert_data(connection, data_batch)
                    data_batch.clear()

            database.mark_url_as_captured(url)

        if data_batch:
            database.batch_insert_data(connection, data_batch)

    connection.close()


if __name__ == "__main__":
    main_func()

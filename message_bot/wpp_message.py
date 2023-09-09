import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import database

class WhatsAppBot():
    def __init__(self):
        self.driver = None

    def init_instance_chrome(self):
        chrome_options = Options()
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox") 
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("user-data-dir=selenium")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("user-agent=User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")
        self.driver = webdriver.Chrome(options=chrome_options)

    def send_messages(self, phone_numbers, message):
        self.driver.set_window_size(1920, 1080)
        for index, phone in enumerate(phone_numbers):
            self.driver.get(f'https://web.whatsapp.com/send?phone={phone}')
            text_box = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, '//div[@role="textbox" and @title="Mensagem"]')))
            text_box.send_keys(message)
            time.sleep(2)
            text_box.send_keys(Keys.ENTER)
            database.update_lead_status_to_captured(phone)

    def quit(self):
        if self.driver:
            self.driver.quit()

bot = WhatsAppBot()

phone_numbers = database.get_phone_leads_ready()
message = 'Olá! Esta é uma mensagem automática!'

while True:
    bot.init_instance_chrome()
    bot.send_messages(phone_numbers, message)
    time.sleep(2)
    bot.quit() 
    # time.sleep(30)

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WhatsAppBot():
    def __init__(self):
        self.driver = None

    def init_instance_chrome(self):
        chrome_options = Options()
        chrome_options.add_argument("--ignore-certificate-errors")
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox") 
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("user-data-dir=selenium")

        self.driver = webdriver.Chrome(options=chrome_options)

    def send_messages(self, phone_numbers, message):

        for phone in phone_numbers:
            self.driver.get(f'https://web.whatsapp.com/send?phone={phone}')
            time.sleep(10)
            text_box = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true" and @title="Mensagem"]')))

            text_box.send_keys(message)
            time.sleep(3)
            text_box.send_keys(Keys.ENTER)
            time.sleep(3) 

    def quit(self):
        if self.driver:
            self.driver.quit()

bot = WhatsAppBot()

phone_numbers = ['4899554102', '4884948169'] 
message = 'Olá! Esta é uma mensagem automática!'

while True:
    bot.init_instance_chrome()
    bot.send_messages(phone_numbers, message)
    bot.quit() 
    time.sleep(30)  

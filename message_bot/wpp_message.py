import subprocess
import psutil
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class WhatsAppBot():

    def __init__(self):
        self.driver = None

    def start_chrome_debugger(self):
        for proc in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
            if 'Google Chrome' in proc.info['name'] and '--remote-debugging-port=9222' in proc.info['cmdline']:
                time.sleep(1)
                print("Chrome com depurador remoto já está em execução.")
                return

        try:
            subprocess.Popen([
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", # Caminho para o Chrome no Mac
                "--remote-debugging-port=9222"
            ])
            time.sleep(5) 
            print("Chrome com depurador remoto iniciado.")
        except FileNotFoundError:
            print("Caminho do Chrome incorreto ou o Chrome não está instalado.")
        except Exception as e:
            print(f"Erro ao iniciar o Chrome: {e}")

    def init_instance_chrome(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        chrome_options.add_argument("--ignore-certificate-errors")


        if not self.driver:
            self.driver = webdriver.Chrome(options=chrome_options)

        return self.driver

    def send_message(self, phone_number, message):
        if not self.driver:
            print("Driver not initialized. Call init_instance_chrome() first.")
            return

        # self.driver.get('https://web.whatsapp.com/')
        # input("Pressione Enter depois de escanear o QR code...")
        self.driver.get(f'https://web.whatsapp.com/send?phone={phone_number}')
        time.sleep(5)
        text_box = self.driver.find_element(By.XPATH, '//div[@contenteditable="true" and @title="Mensagem"]')
        text_box.send_keys(message) 
        time.sleep(3) 
        text_box.send_keys(Keys.ENTER)

    def quit(self):
        if self.driver:
            self.driver.quit()

bot = WhatsAppBot()
bot.start_chrome_debugger()  
bot.init_instance_chrome()   

phone_number = '4899554102' 
message = 'Olá! Esta é uma mensagem automática!'
bot.send_message(phone_number, message)


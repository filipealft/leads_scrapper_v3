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
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox") 
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("user-data-dir=selenium")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("user-agent=User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")
        self.driver = webdriver.Chrome(options=chrome_options)

    def send_messages(self, phone_numbers, message_template):
        self.driver.set_window_size(1920, 1080)
        for phone in phone_numbers:
            segment = database.get_phone_and_segment_for_phone(phone)
            # if segment and segment in INSTAGRAM_LINKS:
            #     instagram_link = INSTAGRAM_LINKS[segment]
            # else:
            #     instagram_link = "https://www.instagram.com/i9nichos/" 

            message = message_template.replace("[Segmento do Estabelecimento]", segment)
            
            self.driver.get(f'https://web.whatsapp.com/send?phone={phone}')
            text_box = WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, '//div[@role="textbox" and @title="Digite uma mensagem"]')))
            text_box.send_keys(message)
            time.sleep(2)
            text_box.send_keys(Keys.ENTER)
            database.update_lead_status_to_captured(phone)

    def quit(self):
        if self.driver:
            self.driver.quit()

bot = WhatsAppBot()

# INSTAGRAM_LINKS = {
#     "loja de bebidas": "https://www.instagram.com/stories/highlights/18020038750661754/?r=1",
#     # "Segmento2": "https://www.instagram.com/link_segmento2",
# }
def remove_non_bmp_chars(s):
    return ''.join(c for c in s if c <= '\uFFFF')

phone_numbers = database.get_phone_leads_ready()
message_template = '''oii tudo bem ?

lucas aqui, da i9 nichos, uma empresa especializada em nichos e móveis sob medida. estava vendo o trabalho de vocês no segmento de [Segmento do Estabelecimento] e pensei que talvez gostariam de conhecer nossos produtos. se curtir a ideia, temos um desconto especial de 10% na primeira compra.

todos os nossos produtos possuem medidas customizáveis, então com certeza teremos algo que te agrade!

se quiser dar uma olhada nas nossas criações, temos um catálogo digital. basta clicar no meu número de telefone aqui no whatsapp apertar no botão "catálogo" para conferir.

dá uma espiada no nosso instagram: https://www.instagram.com/i9nichos/

estamos em florianópolis. se quiser negociar, é só chamar.
'''
# message_template = remove_non_bmp_chars(message_template)

while True:
    bot.init_instance_chrome()
    bot.send_messages(phone_numbers, message_template)
    time.sleep(10)
    bot.quit()

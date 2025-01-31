from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf
import time
import network
import urequests as requests



WIDTH = 128
HEIGHT = 64

i2c = I2C(0, scl = Pin(17), sda = Pin(16), freq=400000)

display = SSD1306_I2C(128, 64, i2c)


# WiFi bağlantı bilgileri
ssid = 'FiberHGW_TP2B50_2.4GHz'
password = 'RVqmddWe'

# WiFi'ya bağlanma fonksiyonu
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        pass
    print('WiFi bağlantısı başarılı:', wlan.ifconfig())

# Döviz kurlarını alma fonksiyonu
def get_exchange_rate(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        print('API isteği başarısız:', response.status_code)
        return None
class wıfıı(framebuf.FrameBuffer):
# Ana program
    def main():
        connect_wifi()
        api_key = 'YOUR_API_KEY'  # Buraya kendi API anahtarınızı girin
        base_currency = 'USD'
        target_currency = 'TRY'
        api_url = f'https://v6.exchangerate-api.com/v6/7af448011e5a80ad2673d73a/latest/{base_currency}'
        
        while True:
            rates = get_exchange_rate(api_url)
            if rates:
                exchange_rate = rates['conversion_rates'][target_currency]
                display.text(f'{base_currency} -> {target_currency}',0,0)
                display.text(f'kuru: {exchange_rate}',0,14)
                display.show()
                display.fill(0)
    
                print(f'{base_currency} -> {target_currency} kuru: {exchange_rate}')
            time.sleep(5)  # Her 60 saniyede bir güncelle

    main()


    

  
    



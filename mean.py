import network
import socket
import machine
import time
from ssd1306 import SSD1306_I2C  # SSD1306 sürücüsünü içe aktarın
from dht import DHT11  # DHT11 kütüphanesini içe aktarın

# WiFi ağı ayarları
SSID = "FiberHGW_TP2B50_2.4GHz"
PASSWORD = "RVqmddWe"

WIDTH = 128
HEIGHT = 64

i2c = machine.I2C(0, scl=machine.Pin(17), sda=machine.Pin(16), freq=400000)

# OLED display initialization
display = SSD1306_I2C(WIDTH, HEIGHT, i2c)

# WiFi bağlantısını başlat
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

# Bağlantının tamamlanmasını bekleyelim
while not wifi.isconnected():
    pass

print("WiFi bağlantısı başarıyla kuruldu")
print("IP adresi:", wifi.ifconfig()[0])

# DHT11 sensörüne bağlı pin tanımlaması
dht_pin = machine.Pin(0)  # GPIO0 pinine bağlı DHT11

# DHT11 sensörü nesnesini oluştur
dht_sensor = DHT11(dht_pin)

# Web sunucusu fonksiyonu
def web_page(temperature):
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>ESP Web Sunucusu</title>
    <meta http-equiv="refresh" content="2"> <!-- Sayfayı her 2 saniyede bir yeniler -->
</head>
<body>
    <h1>ESP Web Sunucusu</h1>
    <p>Sıcaklık: {temperature:.1f} C</p>
</body>
</html>"""
    return html

# Socket oluştur ve sunucuya bağlan
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 8080))  # 80 yerine 8080 portunu kullanıyoruz
s.listen(5)

print("Web sunucusu başlatıldı")

while True:
    # DHT11 üzerinden sıcaklık ve nem ölçümü yap
    dht_sensor.measure()
    temperature = dht_sensor.temperature()

    # OLED ekranı temizle ve sıcaklık verisini yazdır
    display.fill(0)
    display.text('Sicaklik:', 0, 0)
    display.text(f'{temperature:.1f} C', 0, 10)
    display.show()

    # İstemciden gelen istekleri işleme
    conn, addr = s.accept()
    print("Yeni bağlantı:", addr)
    request = conn.recv(1024)
    print("İstek:", request)
    response = web_page(temperature)
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
    
    time.sleep(2)  # 2 saniye bekle


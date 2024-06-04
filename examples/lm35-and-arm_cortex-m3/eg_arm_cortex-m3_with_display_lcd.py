from machine import ADC, Pin, I2C
import time
from i2c_lcd import I2cLcd

# Configuração do ADC
adc = ADC(Pin(34))
adc.atten(ADC.ATTN_11DB)  # Configura a atenuação para leitura até 3.3V
adc.width(ADC.WIDTH_12BIT)  # Resolução de 12 bits

# Configuração do I2C e LCD
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)  # Ajustar o endereço I2C conforme o seu display

def read_temperature():
    adc_value = adc.read()
    voltage = adc_value * (3.3 / 4096.0)
    temperature = voltage * 100.0
    return temperature

lcd.clear()
lcd.move_to(0, 0)
lcd.putstr("Temp: ")

while True:
    temperature = read_temperature()
    lcd.move_to(0, 6)
    lcd.putstr("{:.2f} C".format(temperature))
    time.sleep(1)
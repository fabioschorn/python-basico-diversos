# lcd_api.py
class LcdApi:
    def __init__(self):
        pass

    def clear(self):
        pass

    def move_to(self, col, row):
        pass

    def putstr(self, string):
        pass

# i2c_lcd.py
from lcd_api import LcdApi
from machine import I2C

class I2cLcd(LcdApi):
    def __init__(self, i2c, addr, num_rows, num_cols):
        self.i2c = i2c
        self.addr = addr
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.clear()

    def clear(self):
        self.write_cmd(0x01)

    def move_to(self, col, row):
        pass

    def putstr(self, string):
        pass

    def write_cmd(self, cmd):
        self.i2c.writeto(self.addr, bytearray([0x80, cmd]))

    def write_data(self, data):
        self.i2c.writeto(self.addr, bytearray([0x40, data]))
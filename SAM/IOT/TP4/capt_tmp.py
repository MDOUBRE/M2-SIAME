from smbus2 import SMBus
import time
bus = SMBus(1)

def get_temp2(addr):
    config = [0x00, 0x00]
    bus.write_i2c_block_data(addr, 0x01, config)
    bus.write_byte_data(addr, 0x08, 0x03)

    time.sleep(0.05)

    val = bus.read_i2c_block_data(addr, 0x05, 2)
    
    cval = ((val[0] & 0x1F) * 256) + val[1]
    if cval > 4095 :
        cval -= 8192
    cval = cval * 0.0625
    
    return cval

def read_temp(addr):
    sensor = MCP9808.MCP9808(addr, busnum=1)
    sensor.begin()
    temp = sensor.readTempC()
    print(str(temp))

def get_lum(addr):
    bus.write_byte_data(addr, 0x08, 0x03)
    time.sleep(0.05)
    val = bus.read_word_data(addr, 0xAC)    
    return val


res = get_temp(0x18)
print(res)
res_lum = get_lum(0x39)
print(res_lum)
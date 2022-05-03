#!/usr/bin/python
# -*- coding:utf-8 -*-

import smbus			#import modułu SMBus magistrali I2C
from time import sleep  

#niektóre rejestry czujnika MPU6050 i ich adresy
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47


def MPU_Init():
	#cz. probkowania
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
	#zasilanie
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
	#konfiguracja
	bus.write_byte_data(Device_Address, CONFIG, 0)
	
	#konfiguracja giro.
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	
	#przerwania
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
	#dane przysp. lin. i pr. kąt. 16-bitowe 
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
    
        
        value = ((high << 8) | low)
        
        #znak danych
        if(value > 32768):
                value = value - 65536
        return value


bus = smbus.SMBus(1) 	# lub bus = smbus.SMBus(0) dla starszych wersji
Device_Address = 0x68   # adres urządzenia MPU6050

MPU_Init()

print (" Odczyt danych z akcelerometru i giroskopu")

while True:
	
	#surowe dane z akcelerometru
	acc_x = read_raw_data(ACCEL_XOUT_H)
	acc_y = read_raw_data(ACCEL_YOUT_H)
	acc_z = read_raw_data(ACCEL_ZOUT_H)
	
	#surowe dane z giroskopu
	gyro_x = read_raw_data(GYRO_XOUT_H)
	gyro_y = read_raw_data(GYRO_YOUT_H)
	gyro_z = read_raw_data(GYRO_ZOUT_H)
	
	#skalowanie
	Ax = acc_x/16384.0
	Ay = acc_y/16384.0
	Az = acc_z/16384.0
	
	Gx = gyro_x/131.0
	Gy = gyro_y/131.0
	Gz = gyro_z/131.0
	

	print ("Gx=%.2f" %Gx, "deg/s", "Gy=%.2f" %Gy, "deg/s", "Gz=%.2f" %Gz, "deg/s", "Ax=%.2f g" %Ax, "Ay=%.2f g" %Ay, "Az=%.2f g" %Az) 	
	sleep(1)
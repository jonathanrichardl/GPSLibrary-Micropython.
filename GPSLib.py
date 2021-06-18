# Library GPS MAAT MICROPYTHON
# UNTUK GY-GPS (NEO M6N, NEO M7N)
# Written by : Jonathan Richard, Ervin Halimsurya
import math
import machine
from ucollections import deque
import time
import re
class GPS:
    def __init__(self,rxPin,txPin,baudRate,id = 0):
        self.uart = machine.UART(id = id,baudrate = baudRate, bits = 8, parity = None, stop = 1, tx = machine.Pin(txPin), rx = machine.Pin(rxPin))

    def available(self):
        if(self.uart.any()>0):
            return True
        else:
            return False

    def readData(self):
        while(self.uart.any()>0):
            sentence = self.uart.readline()
            if(sentence.startswith(b"$GNGGA", 0, 7)):
                sentence = sentence.decode('utf-8')
                lat,lat_dir,lon,lon_dir,alt= self.GPGGA(sentence)
                data = "%0.2f,%s,%0.2f,%s,%0.2f"%(lat,lat_dir,lon,lon_dir,alt)
                break
            time.sleep(0.1)
        return data
            

    def dm_to_sd(self,dm):
        '''
        Converts a geographic co-ordinate given in "degrees/minutes" dddmm.mmmm
        format (eg, "12319.943281" = 123 degrees, 19.943281 minutes) to a signed
        decimal (python float) format
        '''
        # '12319.943281'
        if not dm or dm == '0':
            return 0.
        d, m = re.match(r'^(\d+)(\d\d\.\d+)$', dm).groups()
        return float(d) + float(m) / 60

    def latitude(self,lat,lat_dir):
            '''Latitude in signed degrees (python float)'''
            sd = self.dm_to_sd(lat)
            if lat_dir == 'N':
                return +sd
            elif lat_dir == 'S':
                return -sd
            else:
                return 0.

    def longitude(self,lon,lon_dir):
        '''Longitude in signed degrees (python float)'''
        sd = self.dm_to_sd(lon)
        if lon_dir == 'E':
            return +sd
        elif lon_dir == 'W':
            return -sd
        else:
            return 0

    def altitude(self,alt):
        if alt:
            return float(alt)
        else:
            return 0
        
        
    def GPGGA(self,line):
        line = line.split(",")
        lat_raw=line[2]
        lat_dir=line[3]
        lon_raw=line[4]
        lon_dir=line[5]

        res_lat=self.latitude(lat_raw,lat_dir)
        res_lon=self.longitude(lon_raw,lon_dir)
        res_alt=self.altitude(line[9])

        return res_lat,lat_dir,res_lon,lon_dir,res_alt
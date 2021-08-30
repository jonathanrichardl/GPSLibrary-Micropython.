from GPSLib import GPS
gps = GPS(4,5,9600) # rx, tx, baudrate
while True:
    if(gps.available()):
        print(gps.read_data())

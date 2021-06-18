# GPSLibrary-Micropython.
A Micropython Library to efficiently read serial gps and decode the incoming data into Latitude, Longitude, and Altitude. Only GPGGA data is processed.
Written by Jonathan Richard

Department of Electrical Engineering Universitas Indonesia

# Usage 
```
from GPSLib import GPS
gps = GPS(4,5,9600) # RxPin, TxPin, Baudrate
while True:
  if(gps.available()):
     print(gps.readdata())
```

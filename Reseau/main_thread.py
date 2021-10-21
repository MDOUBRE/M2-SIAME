import weather_station_thread as wst
import mqtt_weather as mqtt
import logging as log
import sys

logg=None

if __name__ == "__main__":
    #Creation des fichiers textes
    file = open("illum.txt", "w")
    file.close() 
    file = open("air_press.txt", "w")
    file.close() 
    file = open("hum.txt", "w")
    file.close() 
    file = open("temperature.txt", "w")
    file.close() 

    #logg.basicConfig(format="[%(asctime)s][%(module)s:%(funcName)s:%(lineno)d][%(levelname)s] %(message)s", stream=sys.stdout)
    #logg = logg.getLogger()

    #print("\n[DBG] DEBUG mode activated ... ")
    #logg.setLevel(logg.DEBUG)
    #logg.setLevel(logg.INFO)

    log.info('Weather Station: Start')

    weather_station = wst.WeatherStation()

    if sys.version_info < (3, 0):
        input = raw_input # Compatibility for Python 2.x
    input('Press key to exit\n')

    #mqtt.main()

    if weather_station.ipcon != None:
        weather_station.ipcon.disconnect()

    log.info('Weather Station: End')

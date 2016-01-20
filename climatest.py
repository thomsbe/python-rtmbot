import netatmo
import time

authorization = netatmo.ClientAuth()
devList = netatmo.DeviceList(authorization)

for module, moduleData in devList.lastData(exclude=3600).items() :

    # Name of the module (or station embedded module), the name you defined in the web netatmo account station management
    print(module)

    # List key/values pair of sensor information (eg Humidity, Temperature, etc...)
    for sensor, value in moduleData.items() :
        # To ease reading, print measurement event in readable text (hh:mm:ss)
        if sensor == "When" : value = time.strftime("%H:%M:%S",time.localtime(value))
        print("%30s : %s" % (sensor, value))

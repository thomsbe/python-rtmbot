# coding=utf-8
import netatmo
import time

from fhem import get_fhem, set_fhem

crontable = []
outputs = []


def get_clima():
    authorization = netatmo.ClientAuth()
    devList = netatmo.DeviceList(authorization)
    temp = devList.lastData()['office']['Temperature']
    co2 = devList.lastData()['office']['CO2']
    hum = devList.lastData()['office']['Humidity']
    when = time.strftime("%H:%M:%S", time.localtime(devList.lastData()['office']['When']))
    x_temp = devList.lastData()[u'Auβenraum']['Temperature']
    x_hum = devList.lastData()[u'Auβenraum']['Humidity']
    x_when = time.strftime("%H:%M:%S", time.localtime(devList.lastData()[u'Auβenraum']['When']))
    t_temp = get_fhem('max.t_office_thorsten')['Readings']['temperature']['Value']
    return u'Um {0} war es {1}C, {2}% relative Luftfeuchte und CO2 war bei {3} Schnipsel pro Raummeter.\nHinten beim Thorsten sind es {4}.\nDraußen sind {5}°C und {6}% Luftfeuchte.'.format(
            when, temp, hum, co2, t_temp, x_temp, x_hum)


def get_heizung():
    vorn = get_fhem('max.t_office_vorn')['Readings']['desiredTemperature']['Value']
    mitte = get_fhem('max.t_office_mitte')['Readings']['desiredTemperature']['Value']
    hinten = get_fhem('max.t_office_hinten')['Readings']['desiredTemperature']['Value']
    thorsten = get_fhem('max.t_office_thorsten')['Readings']['desiredTemperature']['Value']

    return u'Heizungseinstellungen\nVorn (Martin): {0}\nMitte (Lisa): {1}\nHinten (Nerdroom): {2}\nThorsten (Sauna): {3}'.format(
        vorn, mitte, hinten, thorsten)


def process_message(data):
    channel = data["channel"]
    text = data["text"]
    if text.startswith("wetter"):
        outputs.append([channel, get_clima()])
    elif text.startswith("heizung"):
        outputs.append([channel, get_heizung()])
    elif text.startswith("heiz"):
        value = text[5:]
        if value.isdigit():
            value = int(float(value))
            if (value > 15 and value < 25):
                set_fhem('set MaxOffice desiredTemperature auto {0}'.format(value))
                outputs.append([channel, 'Ok, ich hab im Office die Heizung auf {0}C gestellt.'.format(value)])
            else:
                outputs.append([channel, 'Vergiss es! Zu warm oder zu kalt.'])
        else:
            outputs.append([channel, 'Eine Zahl! Honk!'])

import json
import urllib2
from urllib import urlencode

import yaml


def get_fhem(device):
    config = yaml.load(file('rtmbot.conf', 'r'))
    _FHEMURL = config['FHEM_URL']
    data = json.load(urllib2.urlopen(_FHEMURL + '?' + urlencode({'cmd':'jsonlist2 ' + device, 'XHR' : 1})))
    if data:
        data = data['Results'][0]
    return data


def set_fhem(cmd):
    config = yaml.load(file('rtmbot.conf', 'r'))
    _FHEMURL = config['FHEM_URL']
    url = _FHEMURL + '?' + urlencode({'cmd' : cmd})
    urllib2.urlopen(url)

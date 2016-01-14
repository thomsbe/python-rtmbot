import json
import os
import sys

from blitzdb import Document, FileBackend

class ListEntry(Document):
    pass

dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
DATABASE = dirname + "/db"

backend = FileBackend(DATABASE)

outputs = []
crontabs = []

def process_message(data):
    channel = data["channel"]
    text = data["text"]

    if text.startswith("shelp"):
        outputs.append([channel,"Shoppinglist! Yeah!\n" +
                       "shop SACHE"])

    if text.startswith("shop"):
        item = text[5:]

        if not item:
            outputs.append([channel, u':fu:'])
        else:
            shopitem = ListEntry({
                "name": item,
                "state": "tobuy"
            })

            backend.save(shopitem)
            backend.commit()
            outputs.append([channel,u'Ok, ich notierte: {0}'.format(item)])

    if text.startswith("slist"):
        shopitems = backend.filter(ListEntry,{'state' : 'tobuy'})
        if not shopitems:
            outputs.append([channel, 'Die Liste ist leer oder ich bin doof.'])
        else:
            c = 1
            for shopitem in shopitems:
                outputs.append([channel, u'{0} {1}'.format(c,shopitem.name)])
                c += 1

    if text.startswith("sdlist"):
        shopitems = backend.filter(ListEntry,{'state' : 'tobuy'})
        if not shopitems:
            outputs.append([channel, 'Die Liste ist leer oder ich bin doof.'])
        else:
            c = 1
            for shopitem in shopitems:
                outputs.append([channel, u'{0} {1} - DEBUG: {2}'.format(c,shopitem.name,shopitem)])
                c += 1

    if text.startswith("sdelall"):
        shopitems = backend.filter(ListEntry,{'state' : 'tobuy'})
        shopitems.delete()
        backend.commit()
        outputs.append([channel, u'So, Liste leer!'])

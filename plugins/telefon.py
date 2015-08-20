import time
import json
crontable = []
outputs = []

def process_message(data):
    channel = data["channel"]
    text = data["text"]
    if text.startswith("debug"):
        outputs.append([channel, 'Ok, ich hab:\n`'+str(data)+'`'])
    if text.startswith("telefon"):
        outputs.append([channel, '+49 351 65616848'])
    
def catch_all(data):
    if not data["type"].startswith("pong"):
        print(data)
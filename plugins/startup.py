import time
outputs = []

def canary():
    #NOTE: you must add a real channel ID for this to work
    outputs.append(["C0457J17K", "Solobot started: " + str(time.time())])

canary()

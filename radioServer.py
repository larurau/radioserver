import mpd
import time

class radioServerClient:
    def __init__(self, adress, port):
        self.adress = adress
        self.port = port
        self.client = mpd.MPDClient()       # create client object, music
        self.connect()
        print("Initial connect server (" + str(adress) + ", " + str(port) + ")")

    def setVolume(self, volume):
        while True:
            try:
                self.client.send_setvol(volume)
                self.client.fetch_setvol(volume)
                break   
            except Exception:
                print("Connection lost while trying to set volume, retry ...")
                #TODO: use ping method of MPDClient to keep connection alive, spawned in another thread
                self.connect()
                time.sleep(1)

    def connect(self):
        while True:
            try:
                self.client.play()
                break
            except Exception:
                self.client.connect(self.adress, self.port)
                time.sleep(1)

    def shutdown(self):
        self.client.close()
        self.client.disconnect()
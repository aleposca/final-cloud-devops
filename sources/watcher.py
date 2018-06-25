import time, requests, re, ntpath
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def getApiKey():
    file=open("/config/config.xml","r")
    str=file.read()

    pattern = r"<apikey>(.*?)</apikey>"
    apikey = re.findall(pattern, str, flags=0)
    return(apikey[0])

def getFileContent(fpath):
    f=open(fpath,"r")
    peerID=f.read()
    return peerID.rstrip()

def updateConfig(event):
    API_ENDPOINT = "http://127.0.0.1:8384/rest/system/config"
    API_KEY = getApiKey()

    HEADERS = {'X-API-Key':API_KEY}
    print(HEADERS)

    name=ntpath.basename(event.src_path)
    peerID=getFileContent(event.src_path)
    print("NAME: %s - PEERID: %s",peerID, peerID)

    PL = '''
{"devices":[{"deviceID":"'''+peerID+'''","name":"'''+name+'''","addresses":["dynamic"],"compression":"metadata","certName":"","introducer":false,"skipIntroductionRemovals":false,"introducedBy":"","paused":false,"allowedNetworks":[],"autoAcceptFolders":true,"maxSendKbps":0,"maxRecvKbps":0}]}
'''
    res = requests.post(API_ENDPOINT, data=PL, headers=HEADERS)

class Watcher:
    DIRECTORY_TO_WATCH = "/watched/"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=False)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print("Received created event - %s." % event.src_path)
            #doingJob(event)
            updateConfig(event)            

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            print("Received modified event - %s." % event.src_path)
            #doingJob(event)
            updateConfig(event)

if __name__ == '__main__':
    w = Watcher()
    w.run()

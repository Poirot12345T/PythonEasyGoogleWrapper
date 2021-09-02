from datetime import datetime
from pytz import utc

def get_time():
    timenow = str(datetime.now(utc)).split("+")[0].replace(" ","T") + "UTC"
    return timenow

class Logger:
    def __init__(self, app_type, message):
        startdate = get_time().split("T")[0]
        self.logname = f"log{app_type}_" + startdate + ".txt"
        logmessage = get_time() + ": " + message
        print(logmessage)
        with open(self.logname, "a") as logfile:
            logfile.write("\n\n" + logmessage)
        
    def log_message(self, message):
        logmessage = get_time() + ": " + message
        print(logmessage)
        with open(self.logname, "a") as logfile:
            logfile.write("\n" + logmessage)
        

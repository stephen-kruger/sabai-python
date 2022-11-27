from assignment import Assignment
import json

class DhcpdLease:
    name = ""
    ip = ""
    mac = ""
    date = ""

    def __init__(self, data):
        self.name = data[0]
        self.ip = data[1]
        self.mac = data[2]
        self.date = data[3]


#dhcpdLease = DhcpdLease(json.loads("['Stephens-MBP','192.168.199.169','B0:DE:28:0E:48:A0','0 days, 23:47:57']".replace("'","\"")))

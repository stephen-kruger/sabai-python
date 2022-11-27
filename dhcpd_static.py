from assignment import Assignment

class DhcpdStatic:
    mac = ""
    name = ""
    ip = ""
    xxx = ""
    assignment = Assignment.UNKNOWN

    def __init__(self, str):
        self.mac = str.split("<")[0]
        self.ip = str.split("<")[1]
        self.name = str.split("<")[2]
        #xxx = str.split("<")[3]
        self.assignment = Assignment(str.split("<")[4])

#obj = DhcpdStatic("00:01:2E:A0:BE:CD<192.168.199.2<vpna<0<1")

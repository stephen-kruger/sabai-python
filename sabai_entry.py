from assignment import Assignment

class SabaiEntry:
    mac = ""
    ip = ""
    name = ""
    assignment = Assignment.UNKNOWN

    def __init__(self, mac, ip, name, assignment):
        self.mac = mac
        self.ip = ip
        self.name = name
        self.assignment = assignment
